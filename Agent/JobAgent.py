from typing import Optional, Any, Dict, List
from browser_use import Agent, Browser, Controller, ActionResult
from browser_use.browser.context import BrowserContext
from langchain_openai import ChatOpenAI
import logging

class JobAgent:
    def __init__(
        self,
        task: str,
        llm: ChatOpenAI,
        browser: BrowserContext,
        controller: Controller,
        sensitive_data: Optional[Dict[str, Any]] = None,
        initial_actions: Optional[List[Dict[str, Any]]] = None,
        hook_end =None,
        hook_boolean = None 
    ):
        self.task = task
        self.llm = llm
        self.browser = browser
        self.controller = controller if controller is not None else Controller()
        self.sensitive_data = sensitive_data if sensitive_data is not None else {}
        self.initial_actions = initial_actions if initial_actions is not None else []
        self.job_apply_agent = None
        self.on_step_end = hook_end
        self.hook_boolean = hook_boolean

    def initiate_agent_task(self) -> None:
        try:
            self.job_apply_agent = Agent(
                browser_context=self.browser,
                task=self.task,
                initial_actions=self.initial_actions,
                llm=self.llm,
                use_vision=True,
                controller=self.controller,
                sensitive_data=self.sensitive_data , # Uncommented this line
            )
        except Exception as e:
            logging.error(f"Failed to initcleialize agent: {e}")
            raise

    async def run_agent(self):
        if not self.job_apply_agent:
            raise RuntimeError("Agent not initialized. Call initiate_agent_task() first.")
        try:
            if self.hook_boolean is None:
                
                self.history = await self.job_apply_agent.run()
            else:
                self.history = await self.job_apply_agent.run(
                    on_step_end=self.on_step_end,
                    max_steps = 20
                )
            return self.job_apply_agent.browser_context
        except Exception as e:
            logging.error(f"Error running agent: {e}")
            raise

# Returns the browser_context that we were using for previous context 
    def browser_context(self) -> BrowserContext:
        return self.job_apply_agent.browser_context
