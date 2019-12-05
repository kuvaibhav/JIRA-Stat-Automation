from .jsonreader import ReadJiraIssues # Adaptee

from .jira_dump_reader import  CalculateJIRAStats # Target

def report_generator(jira_issues: ReadJiraIssues):
    jira_issues.fetch_jira_tickets()

class JIRAAdapter(ReadJiraIssues):

    def __init__(self, calculate_jira_status:CalculateJIRAStats):
        self.calculate_jira_status = calculate_jira_status

    def fetch_jira_tickets(self):
        self.calculate_jira_status.generate_report()
