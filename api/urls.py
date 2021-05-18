from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('time', views.time, name='time'),
    # ----------------- lessons query URLs ----------------------
    path('manager/lessons/state', views.ManagerLessonsUpdate.as_view()),
    # ----------------- classrooms query URLs ----------------------
    path('parent/classrooms', views.ParentClassroomList.as_view()),
    path('student/classrooms', views.StudentClassroomList.as_view()),
    path('teacher/classrooms', views.TeacherClassroomList.as_view()),
    path('manager/classrooms', views.ManagerClassroomList.as_view()),
    # ----------------- everything in class sheet URLs -------------
    path('student/<int:class_id>/class-sheet', views.StudentClassSheetList.as_view()),
    path('teacher/<int:class_id>/class-sheet', views.TeacherClassSheetList.as_view()),
    path('manager/<int:class_id>/class-sheet', views.ManagerClassSheetList.as_view()),
    # ----------------- Quize & Scores URLs ------------------------
    path('teacher/quiz', views.TeacherQuizList.as_view()),
    path('teacher/quiz/<int:pk>', views.TeacherQuizDetail.as_view()),
    path('teacher/<int:meeting>/quiz/<int:quiz>', views.TeacherCreateQuizeStudentsList.as_view()),
    path('student/<int:meeting>/quiz/<int:quiz>', views.StudentQuizDetail.as_view()),
    path('student/<int:meeting>/quiz/<int:quiz>/response', views.StudentQuizScoreUpdate.as_view()),
    path('student/<int:class_id>/score', views.StudentQuizScoreList.as_view()),
    path('teacher/<int:class_id>/score', views.TeacherQuizScoreList.as_view()),
    path('manager/<int:class_id>/score', views.ManagerQuizScoreList.as_view()),
    path('manager/<int:class_id>/score2', views.AlternateManagerQuizScoreList),
    # ----------------- Exam URLs ---------------------------------
    path('parent/exam', views.ParentExamList.as_view()),
    path('student/exam', views.StudentExamList.as_view()),
    path('teacher/exam', views.TeacherExamList.as_view()),
    path('manager/exam', views.ManagerExamList.as_view()),
    path('manager/exam/<int:pk>', views.ManagerExamDetails.as_view()),
    path('teacher/exam_meeting', views.ExamMeetingList.as_view()),
    path('teacher/exam_meeting/<int:exam_meeting_id>/end', views.ExamMeetingEnd.as_view()),
    path('teacher/exam_meeting/token/<str:token>', views.TeacherExamMeetingByTokenList.as_view()),
    path('student/exam_meeting/token/<str:token>', views.StudentExamMeetingByTokenList.as_view()),
    path('parent/<int:class_id>/exam_score', views.ParentExamScoreList.as_view()),
    path('student/<int:class_id>/exam_score', views.StudentExamScoreList.as_view()),
    path('teacher/<int:class_id>/exam_score', views.TeacherExamScoreList.as_view()),
    path('manager/<int:class_id>/exam_score', views.ManagerExamScoreList.as_view()),
    # ----------------- Presence Absence URLs ---------------------
    path('teacher/class-meeting-sheet/<int:class_meeting_id>', views.TeacherCreatePresenceAbsenceSheet.as_view()),
    path('teacher/class-meeting-sheet/<int:class_meeting_id>/entrance-presence/<int:student_id>', views.TeacherSubmitEntrancePresence.as_view()),
    path('teacher/class-meeting-sheet/<int:class_meeting_id>/verify-presence/<int:student_id>', views.TeacherSubmitVerifiedPresence.as_view()),
    path('teacher/class-meeting-sheet/<int:class_meeting_id>/verify-presence', views.TeacherSubmitVerifiedPresenceList.as_view()),
    # path('student/<int:class_id>/presence-absence', views.StudentPresenceAbsenceList.as_view()),
    # path('teacher/<int:class_id>/presence-absence', views.TeacherPresenceAbsenceList.as_view()),
    # path('manager/<int:class_id>/presence-absence', views.ManagerPresenceAbsenceList.as_view()),
    # ----------------- Presence Absence per class meeting URLs -----------
    path('teacher/<int:class_meeting_id>/classmeeting-presence-absence', views.TeacherPresenceAbsenceClassMeetingList.as_view()),
    # ----------------- Disciplinary Notes Per Day URLs -----------
    path('teacher/class-meeting-sheet/<int:class_id>/per-day-disciplinary-note', views.TeacherSubmitDisciplinaryPerDay.as_view()),
    path('teacher/class-meeting-sheet/<int:class_id>/per-day-disciplinary-note/<int:pk>', views.TeacherSubmitDisciplinaryPerDayDetails.as_view()),
    # ----------------- Meeting scores Per Day URLs ---------------
    path('teacher/class-meeting-sheet/<int:class_id>/per-day-meeting-score', views.TeacherSubmitMeetingScorePerDay.as_view()),
    path('teacher/class-meeting-sheet/<int:class_id>/per-day-meeting-score/<int:pk>', views.TeacherSubmitMeetingScorePerDayDetails.as_view()),
    # ----------------- Per Day Classsheet URLs -------------------
    path('parent/class-meeting-sheet/<int:class_id>/per-day', views.ParentPerDayClassSheetList.as_view()),
    path('student/class-meeting-sheet/<int:class_id>/per-day', views.StudentPerDayClassSheetList.as_view()),
    path('teacher/class-meeting-sheet/<int:class_id>/per-day', views.TeacherPerDayClassSheetList.as_view()),
    path('manager/class-meeting-sheet/<int:class_id>/per-day', views.ManagerPerDayClassSheetList.as_view()),
    # ----------------- Per Day Presence Absence URLs -------------------
    # path('student/class-meeting-sheet/<int:class_id>/per-day-presence-absence', views.StudentPerDayPresenceAbsenceList.as_view()),
    # path('teacher/class-meeting-sheet/<int:class_id>/per-day-presence-absence', views.TeacherPerDayPresenceAbsenceList.as_view()),
    # path('manager/class-meeting-sheet/<int:class_id>/per-day-presence-absence', views.ManagerPerDayPresenceAbsenceList.as_view()),
    path('parent/<int:class_id>/presence-absence', views.ParentPerDayPresenceAbsenceList.as_view()),
    path('student/<int:class_id>/presence-absence', views.StudentPerDayPresenceAbsenceList.as_view()),
    path('teacher/<int:class_id>/presence-absence', views.TeacherPerDayPresenceAbsenceList.as_view()),
    path('manager/<int:class_id>/presence-absence', views.ManagerPerDayPresenceAbsenceList.as_view()),
    # ----------------- Meeting scores URLs -----------------------
    path('teacher/class-meeting-sheet/<int:class_meeting_id>/meeting-score/<int:student_id>', views.TeacherSubmitMeetingScore.as_view()),
    path('student/<int:class_id>/meeting-score', views.StudentMeetingScoreList.as_view()),
    path('teacher/<int:class_id>/meeting-score', views.TeacherMeetingScoreList.as_view()),
    path('manager/<int:class_id>/meeting-score', views.ManagerMeetingScoreList.as_view()),
    # ----------------- Disciplinary Notes URLs -------------------
    path('teacher/class-meeting-sheet/<int:class_meeting_id>/disciplinary-note/<int:student_id>', views.TeacherSubmitDisciplinaryNote.as_view()),
    path('student/<int:class_id>/disciplinary-note', views.StudentDisciplinaryNoteList.as_view()),
    path('teacher/<int:class_id>/disciplinary-note', views.TeacherDisciplinaryNoteList.as_view()),
    path('manager/<int:class_id>/disciplinary-note', views.ManagerDisciplinaryNoteList.as_view()),
    # ----------------- Homework URLs -----------------------------
    path('teacher/homework', views.TeacherHomeworkList.as_view()),
    path('teacher/homework/<int:pk>', views.TeacherHomeworkDetails.as_view()),
    path('student/response-homework/<int:pk>', views.StudentHomeworkResponseUpload.as_view()),
    path('student/<int:class_id>/homework', views.StudentHomeworkResponseList.as_view()),
    path('teacher/<int:class_id>/homework', views.TeacherHomeworkResponseList.as_view()),
    path('manager/<int:class_id>/homework', views.ManagerHomeworkResponseList.as_view()),
    # ----------------- Teacher TimeLine URLs ---------------------
    path('manager/teacher_times/<int:teacher_id>', views.ManagerTeacherAvailabilityList.as_view()),
    path('manager/teacher_times/<int:teacher_id>/<int:pk>', views.ManagerTeacherAvailabilityDetails.as_view()),
    path('manager/teacher_times/section_reserved/<int:teacher_id>', views.ManagerTeacherReservedSectionsList.as_view()),
    path('teacher/times', views.TeacherTeacherAvailabilityList.as_view()),
    path('teacher/times/<int:pk>', views.TeacherTeacherAvailabilityToggleStatus.as_view()),
    path('teacher/times/section_reserved', views.TeacherTeacherReservedSectionsList.as_view()),
    # ----------------- Teacher Lessons URLs ---------------------
    path('manager/teacher_lessons', views.ManagerTeacherLessonsList.as_view()),
    path('manager/teacher_lessons/<int:pk>', views.ManagerTeacherLessonsDelete.as_view()),
    # ----------------- Teacher Lessons From sections URLs ---------------------
    path('teacher/lessons', views.TeacherLessonsFromSection.as_view()),
    # ----------------- Parent Child URLs ---------------------
    path('manager/parent_child', views.ManagerParentChildCreate.as_view()),
    path('manager/parent_child/<int:parent_id>', views.ManagerParentChildList.as_view()),
    # path('manager/parent_child/delete/<int:pk>', views.ManagerParentChildDetail.as_view()),
    path('parent/parent_child', views.ParentParentChildList.as_view()),
    # ----------------- Parent dashboard URLs ---------------------
    path('parent/dashboards', views.ParentDashboardsList.as_view()),
    # ----------------- Parent schedule URLs ---------------------
    path('parent/schedules', views.ParentScheduleList.as_view()),
    # ----------------- Student schedule URLs ---------------------
    path('student/schedules/my', views.StudentSchedulesList.as_view()),
    # ----------------- Student schedule URLs ---------------------
    path('max_du', views.DiskUsageList.as_view()),
    path('save_video', views.SavedVideosCreate.as_view()),
    path('teacher/can_record', views.CanRecordVideo.as_view()),
    path('parent/recorded-videos', views.ParentPerDayVideosList.as_view()),
    path('student/recorded-videos', views.StudentPerDayVideosList.as_view()),
    path('teacher/recorded-videos', views.TeacherPerDayVideosList.as_view()),
    path('manager/recorded-videos', views.ManagerPerDayVideosList.as_view()),
    # ----------------- Reports URLs ---------------------
    path('manager/report/presence-absence', views.ManagerPresenceAbsenceReport.as_view(), name='manager_report_presence-absence'),
    path('manager/report/presence-absence-perclass', views.ManagerPresenceAbsencePerClassReport.as_view(), name='manager_report_presence-absence_perclass'),
    path('manager/report/score-perclass', views.ManagerScorePerClassReport.as_view(), name='manager_report_score_perclass'),
]