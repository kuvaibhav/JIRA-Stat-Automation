import xlrd


class CalculateJIRAStats(object):

    def __init__(self):
        # give JIRA dumps path
        path = 'dumps.xlsx'
        # give resolved date
        resolved_date = ''
        jira_issue_list = []
        input_work_book = xlrd.open_workbook(path)
        input_work_sheet = input_work_book.sheet_by_index(1)
        for i in range(1, input_work_sheet.nrows):
            current_row = input_work_sheet.row_values(i, 0, 100)
            jira_issue_object = {'jira_id': int(input_work_sheet.cell_value(i, 2)), 'assigned_to': input_work_sheet.cell_value(i, 13),
                                 'priority': self.calculate_priority(current_row),
                                 'application': self.calculate_application(current_row),
                                 'isEnhancement': self.find_if_enhancement(current_row), 'status': input_work_sheet.cell_value(i, 4)}
            jira_issue_list.append(jira_issue_object)
        jira_issues = []
        jira_enhancements = []
        for object in jira_issue_list:
            if object['isEnhancement']:
                jira_enhancements.append(object)
            else:
                jira_issues.append(object)

        print(jira_enhancements)
        populate_stat_issues = PopulateStats('Issues', jira_issues)
        populate_stat_issues.print_report()
        populate_stat_enhancements = PopulateStats('Enhancements', jira_enhancements)
        populate_stat_enhancements.print_report()

    @staticmethod
    def calculate_priority(excel_row_array):
        track_priority_occurrence = False
        priority = 'NA'
        for i in range(len(excel_row_array)):
            if excel_row_array[i] == 'P1' or excel_row_array[i] == 'P2' or excel_row_array[i] == 'P3':
                track_priority_occurrence = True
                priority = excel_row_array[i]
                if track_priority_occurrence:
                    return priority
        if not track_priority_occurrence:
            raise Exception('Jira Ticket {} does not have any Priority assigned. For correct report priority'
                            'needs to be assigned'.format(excel_row_array[1]))
        return priority

    @staticmethod
    def calculate_application(excel_row_array):
        track_application_occurrence = False
        application = 'NA'
        for i in range(len(excel_row_array)):
            if excel_row_array[i] in ['UC1', 'UC2', 'UC3', 'UC4', 'UC5', 'UC6', 'uc1', 'uc2', 'uc3',
                                      'uc4', 'uc5', 'uc6']:
                track_application_occurrence = True
                application = excel_row_array[i]
                if track_application_occurrence:
                    return application
        if not track_application_occurrence:
            raise Exception('Jira Ticket {} does not have application name against it.'.
                            format(excel_row_array[1]))
        return application

    @staticmethod
    def find_if_enhancement(excel_row_array):
        """
            To find an enhancement we need to look at below occurrence:
            'Issue_Type_Issue' return False
            'Issue_Type_Enhancements' return True
            'Issue_Type_Additional_Requirements' return True
             If nothing is found look for
             Return as Issue i.e. False
        """
        for i in range(len(excel_row_array)):
            if excel_row_array[i] in ['Issue_Type_Enhancements', 'Issue_Type_Additional_Requirements']:
                return True
            elif excel_row_array[i] == 'Issue_Type_Issue':
                return False
        return False


class PopulateStats(object):
    def __init__(self, defect_type, jira_object):
        self.defect_type = defect_type
        self.jira_object = jira_object

    def print_report(self):
        print('----------------------------------' + self.defect_type + '----------------------------------')
        print('-------------------------------------------------------------------------------------')
        print('---------------------------------------USE CASE 1------------------------------------')
        print('---------Blocked---------Not Started---------In Progress----------UAT----------Closed')
        self.user_case_specific_stat('UC1')
        print('-------------------------------------------------------------------------------------')
        print('---------------------------------------USE CASE 2------------------------------------')
        print('---------Blocked---------Not Started---------In Progress----------UAT----------Closed')
        self.user_case_specific_stat('UC2')
        print('-------------------------------------------------------------------------------------')
        print('---------------------------------------USE CASE 3------------------------------------')
        print('---------Blocked---------Not Started---------In Progress----------UAT----------Closed')
        self.user_case_specific_stat('UC3')
        print('-------------------------------------------------------------------------------------')
        print('---------------------------------------USE CASE 4------------------------------------')
        print('---------Blocked---------Not Started---------In Progress----------UAT----------Closed')
        self.user_case_specific_stat('UC4')
        print('-------------------------------------------------------------------------------------')
        print('---------------------------------------USE CASE 5------------------------------------')
        print('---------Blocked---------Not Started---------In Progress----------UAT----------Closed')
        self.user_case_specific_stat('UC5')
        print('-------------------------------------------------------------------------------------')
        print('---------------------------------------USE CASE 6------------------------------------')
        print('---------Blocked---------Not Started---------In Progress----------UAT----------Closed')
        self.user_case_specific_stat('UC6')

    def user_case_specific_stat(self, use_case):
        use_case_wise_jira_list = []
        for jiraobject in self.jira_object:
            if jiraobject['application'] == use_case:
                use_case_wise_jira_list.append(jiraobject)
        self.process_stat(use_case_wise_jira_list)

    def process_stat(self, usecase_jira_list):
        p1_jira_tickets = []
        p2_jira_tickets = []
        p3_jira_tickets = []
        for jiraobject in usecase_jira_list:
            if jiraobject['priority'] == 'P1':
                p1_jira_tickets.append(jiraobject)
            elif jiraobject['priority'] == 'P2':
                p2_jira_tickets.append(jiraobject)
            elif jiraobject['priority'] == 'P3':
                p3_jira_tickets.append(jiraobject)
            else:
                raise Exception('Stats cannot be generated as Jira Ticket {} does not have any priority'
                                .format(jiraobject['jira_id']))
        blocked = 0
        not_started = 0
        in_progress = 0
        uat = 0
        closed = 0
        for ticket in p1_jira_tickets:
            if ticket['status'] == 'New Requests':
                not_started = not_started + 1
            elif ticket['status'] == 'Done':
                closed = closed + 1
            elif ticket['status'] == 'Blocked':
                blocked = blocked + 1
            elif ticket['status'] == 'UAT':
                uat = uat + 1
            else:
                in_progress = in_progress + 1
        print('P1          ' + str(blocked) + '                    ' + str(not_started) + '                  '
              + str(in_progress) + '            ' + str(uat) + '             ' + str(closed))
        blocked = 0
        not_started = 0
        in_progress = 0
        uat = 0
        closed = 0
        for ticket in p2_jira_tickets:
            if ticket['status'] == 'New Requests' or ticket['status'] == 'Backlog':
                not_started = not_started + 1
            elif ticket['status'] == 'Done':
                closed = closed + 1
            elif ticket['status'] == 'Blocked':
                blocked = blocked + 1
            elif ticket['status'] == 'UAT':
                uat = uat + 1
            else:
                in_progress = in_progress + 1
        print('P2          ' + str(blocked) + '                    ' + str(not_started) + '                  '
              + str(in_progress) + '            ' + str(uat) + '             ' + str(closed))
        blocked = 0
        not_started = 0
        in_progress = 0
        uat = 0
        closed = 0
        for ticket in p3_jira_tickets:
            if ticket['status'] == 'New Requests' or ticket['status'] == 'Backlog':
                not_started = not_started + 1
            elif ticket['status'] == 'Done':
                closed = closed + 1
            elif ticket['status'] == 'Blocked':
                blocked = blocked + 1
            elif ticket['status'] == 'UAT':
                uat = uat + 1
            else:
                in_progress = in_progress + 1
        print('P3          ' + str(blocked) + '                    ' + str(not_started) + '                  '
              + str(in_progress) + '            ' + str(uat) + '             ' + str(closed))


if __name__ == '__main__':
    CalculateJIRAStats()
