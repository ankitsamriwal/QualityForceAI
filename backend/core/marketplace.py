"""
Agent Marketplace - Central hub for managing and executing testing agents
"""
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
import uuid
import logging

from core.models import (
    AgentType, AgentMetadata, AgentInput,
    AgentExecutionResult, ExecutionRequest, BatchExecutionRequest,
    ExecutionStatus
)
from agents import (
    UnitTestingAgent,
    FunctionalTestingAgent,
    IntegrationTestingAgent,
    SecurityTestingAgent,
    LoadTestingAgent,
    StressTestingAgent,
    RegressionTestingAgent
)

logger = logging.getLogger(__name__)


class AgentMarketplace:
    """
    Marketplace for managing and executing testing agents.
    Supports concurrent execution of multiple agents.
    """

    def __init__(self):
        self.agents: Dict[AgentType, type] = {}
        self.active_executions: Dict[str, asyncio.Task] = {}
        self.execution_results: Dict[str, AgentExecutionResult] = {}
        self.execution_lock = asyncio.Lock()

        # Register all available agents
        self._register_agents()

    def _register_agents(self):
        """Register all available testing agents"""
        self.agents[AgentType.UNIT_TESTING] = UnitTestingAgent
        self.agents[AgentType.FUNCTIONAL_TESTING] = FunctionalTestingAgent
        self.agents[AgentType.INTEGRATION_TESTING] = IntegrationTestingAgent
        self.agents[AgentType.SECURITY_TESTING] = SecurityTestingAgent
        self.agents[AgentType.LOAD_TESTING] = LoadTestingAgent
        self.agents[AgentType.STRESS_TESTING] = StressTestingAgent
        self.agents[AgentType.REGRESSION_TESTING] = RegressionTestingAgent

        logger.info(f"Registered {len(self.agents)} testing agents")

    def get_all_agents(self) -> List[AgentMetadata]:
        """Get metadata for all available agents"""
        metadata_list = []

        for agent_class in self.agents.values():
            agent = agent_class()
            metadata_list.append(agent.get_metadata())

        return metadata_list

    def get_agent_metadata(self, agent_type: AgentType) -> Optional[AgentMetadata]:
        """Get metadata for a specific agent"""
        if agent_type not in self.agents:
            return None

        agent = self.agents[agent_type]()
        return agent.get_metadata()

    async def execute_agent(
        self,
        agent_type: AgentType,
        inputs: AgentInput,
        config: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Execute a single agent asynchronously.
        Returns execution_id for tracking.
        """
        if agent_type not in self.agents:
            raise ValueError(f"Agent type {agent_type} not found")

        # Create agent instance
        agent_class = self.agents[agent_type]
        agent = agent_class()

        # Create execution task
        execution_id = str(uuid.uuid4())

        async def run_agent():
            try:
                logger.info(f"Starting execution {execution_id} for {agent_type}")
                result = await agent.execute(inputs, config)
                result.execution_id = execution_id

                async with self.execution_lock:
                    self.execution_results[execution_id] = result

                logger.info(f"Completed execution {execution_id}")
                return result
            except Exception as e:
                logger.error(f"Execution {execution_id} failed: {str(e)}")
                error_result = AgentExecutionResult(
                    execution_id=execution_id,
                    agent_type=agent_type,
                    status=ExecutionStatus.FAILED,
                    start_time=datetime.now(),
                    end_time=datetime.now(),
                    error_message=str(e)
                )

                async with self.execution_lock:
                    self.execution_results[execution_id] = error_result

                return error_result

        # Start execution task
        task = asyncio.create_task(run_agent())

        async with self.execution_lock:
            self.active_executions[execution_id] = task

        return execution_id

    async def execute_batch(
        self,
        batch_request: BatchExecutionRequest
    ) -> Dict[str, str]:
        """
        Execute multiple agents concurrently or sequentially.
        Returns mapping of agent_type to execution_id.
        """
        execution_ids = {}

        if batch_request.parallel:
            # Execute all agents concurrently
            logger.info(f"Executing {len(batch_request.executions)} agents in parallel")

            tasks = []
            for exec_request in batch_request.executions:
                task = self.execute_agent(
                    exec_request.agent_type,
                    exec_request.inputs,
                    exec_request.config
                )
                tasks.append((exec_request.agent_type, task))

            # Wait for all executions to start
            for agent_type, task in tasks:
                execution_id = await task
                execution_ids[agent_type.value] = execution_id

        else:
            # Execute agents sequentially
            logger.info(f"Executing {len(batch_request.executions)} agents sequentially")

            for exec_request in batch_request.executions:
                try:
                    execution_id = await self.execute_agent(
                        exec_request.agent_type,
                        exec_request.inputs,
                        exec_request.config
                    )
                    execution_ids[exec_request.agent_type.value] = execution_id

                    # Wait for completion before starting next
                    await self.wait_for_completion(execution_id)

                    # Check if we should continue on failure
                    result = self.get_execution_result(execution_id)
                    if result and result.status == ExecutionStatus.FAILED:
                        if not batch_request.continue_on_failure:
                            logger.warning("Stopping batch execution due to failure")
                            break

                except Exception as e:
                    logger.error(f"Failed to execute {exec_request.agent_type}: {str(e)}")
                    if not batch_request.continue_on_failure:
                        break

        return execution_ids

    async def wait_for_completion(self, execution_id: str, timeout: Optional[float] = None):
        """Wait for an execution to complete"""
        if execution_id not in self.active_executions:
            return

        try:
            await asyncio.wait_for(
                self.active_executions[execution_id],
                timeout=timeout
            )
        except asyncio.TimeoutError:
            logger.warning(f"Execution {execution_id} timed out")
            await self.cancel_execution(execution_id)

    async def cancel_execution(self, execution_id: str) -> bool:
        """Cancel a running execution"""
        if execution_id not in self.active_executions:
            return False

        task = self.active_executions[execution_id]
        task.cancel()

        try:
            await task
        except asyncio.CancelledError:
            logger.info(f"Cancelled execution {execution_id}")

        # Update result status
        if execution_id in self.execution_results:
            self.execution_results[execution_id].status = ExecutionStatus.CANCELLED

        return True

    def get_execution_status(self, execution_id: str) -> Optional[ExecutionStatus]:
        """Get the status of an execution"""
        if execution_id in self.execution_results:
            return self.execution_results[execution_id].status

        if execution_id in self.active_executions:
            return ExecutionStatus.RUNNING

        return None

    def get_execution_result(self, execution_id: str) -> Optional[AgentExecutionResult]:
        """Get the result of an execution"""
        return self.execution_results.get(execution_id)

    def get_all_executions(self) -> List[AgentExecutionResult]:
        """Get all execution results"""
        return list(self.execution_results.values())

    def get_active_execution_count(self) -> int:
        """Get count of currently running executions"""
        return len([
            task for task in self.active_executions.values()
            if not task.done()
        ])

    async def shutdown(self):
        """Shutdown marketplace and cancel all running executions"""
        logger.info("Shutting down marketplace")

        # Cancel all active executions
        for execution_id in list(self.active_executions.keys()):
            await self.cancel_execution(execution_id)

        # Clear state
        self.active_executions.clear()
        logger.info("Marketplace shutdown complete")
