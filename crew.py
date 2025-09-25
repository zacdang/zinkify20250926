import os

from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
	EXASearchTool,
	ScrapegraphScrapeTool
)






@CrewBase
class WorksenseCompassCrew:
    """WorksenseCompass crew"""
    
    @agent
    def chat_bot(self) -> Agent:
        return Agent(
            config=self.agents_config["chat_bot"],
            tools=[],
            reasoning=True,
            max_reasoning_attempts=3,
            inject_date=True,
            allow_delegation=False,
            max_iter=10,
            max_rpm=None,
            max_execution_time=30,
            llm=LLM(
                model="gpt-4",
                temperature=0.7,
            ),
        )

    
    @agent
    def agent_2_3(self) -> Agent:

        
        return Agent(
            config=self.agents_config["agent_2_3"],
            
            
            tools=[
				ScrapegraphScrapeTool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=10,
            max_rpm=None,
            max_execution_time=30,
            llm=LLM(
                model="gpt-4o",
                temperature=0.2,
            ),
            
        )
    
    @agent
    def agent_1(self) -> Agent:

        
        return Agent(
            config=self.agents_config["agent_1"],
            
            
            tools=[

            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def agent_2_1(self) -> Agent:

        
        return Agent(
            config=self.agents_config["agent_2_1"],
            
            
            tools=[
				EXASearchTool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=10,
            max_rpm=None,
            max_execution_time=60,
            llm=LLM(
                model="gpt-4o",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def agent_2_2(self) -> Agent:

        
        return Agent(
            config=self.agents_config["agent_2_2"],
            
            
            tools=[
				EXASearchTool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=10,
            max_rpm=None,
            max_execution_time=30,
            llm=LLM(
                model="gpt-4.1",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def report_compiler(self) -> Agent:

        
        return Agent(
            config=self.agents_config["report_compiler"],
            
            
            tools=[

            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o",
                temperature=0.0,
            ),
            
        )
    

    
    @task
    def classify_issues_from_url_and_user_question(self) -> Task:
        return Task(
            config=self.tasks_config["classify_issues_from_url_and_user_question"],
            markdown=False,
            
            
        )
    
    @task
    def analyze_cross_functional_issues(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_cross_functional_issues"],
            markdown=False,
            
            
        )
    
    @task
    def research_company_policy_solutions(self) -> Task:
        return Task(
            config=self.tasks_config["research_company_policy_solutions"],
            markdown=False,
            
            
        )
    
    @task
    def analyze_soft_skills_gaps(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_soft_skills_gaps"],
            markdown=False,
            
            
        )
    
    @task
    def compile_final_report(self) -> Task:
        return Task(
            config=self.tasks_config["compile_final_report"],
            markdown=False,
            
            
        )
    

    @crew
    def crew(self) -> Crew:
        """Creates the WorksenseCompass crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )

    def _load_response_format(self, name):
        with open(os.path.join(self.base_directory, "config", f"{name}.json")) as f:
            json_schema = json.loads(f.read())

        return SchemaConverter.build(json_schema)
