from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from .tools import QuotationLogicTool

@CrewBase
class VoithruFactoryCrew():
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def receptionist(self) -> Agent:
        return Agent(config=self.agents_config['receptionist'], verbose=True)

    @agent
    def price_optimizer(self) -> Agent:
        return Agent(config=self.agents_config['price_optimizer'], tools=[QuotationLogicTool()], verbose=True)

    @agent
    def communication_manager(self) -> Agent:
        return Agent(config=self.agents_config['communication_manager'], verbose=True)

    @task
    def filter_email_task(self) -> Task:
        return Task(config=self.tasks_config['filter_email_task'])

    @task
    def calculate_quote_task(self) -> Task:
        return Task(config=self.tasks_config['calculate_quote_task'])

    @task
    def notify_manager_task(self) -> Task:
        return Task(config=self.tasks_config['notify_manager_task'])

    @task
    def send_to_client_task(self) -> Task:
        return Task(config=self.tasks_config['send_to_client_task'])

    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks, process=Process.sequential, verbose=True)