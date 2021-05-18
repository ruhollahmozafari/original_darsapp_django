# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Action(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_by_user = models.CharField(max_length=255, blank=True, null=True)
    deleted = models.TextField(blank=True, null=True)  # This field type is a guess.
    modified_by_user = models.CharField(max_length=255, blank=True, null=True)
    actions_group_id = models.BigIntegerField(blank=True, null=True)
    code = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'action'


class ActionsGroup(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_by_user = models.CharField(max_length=255, blank=True, null=True)
    deleted = models.TextField(blank=True, null=True)  # This field type is a guess.
    modified_by_user = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'actions_group'


class ActionsGroupActions(models.Model):
    actions_group = models.ForeignKey(ActionsGroup, models.DO_NOTHING)
    actions = models.BigIntegerField(blank=True, null=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        # managed = False
        db_table = 'actions_group_actions'


class ClassNote(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_by_user = models.CharField(max_length=255, blank=True, null=True)
    deleted = models.TextField(blank=True, null=True)  # This field type is a guess.
    modified_by_user = models.CharField(max_length=255, blank=True, null=True)
    class_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'class_note'


class ConvertedImage(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_by_user = models.CharField(max_length=255, blank=True, null=True)
    deleted = models.TextField(blank=True, null=True)  # This field type is a guess.
    modified_by_user = models.CharField(max_length=255, blank=True, null=True)
    path = models.CharField(max_length=255, blank=True, null=True)
    resource_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'converted_image'


class DayPoint(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_by_user = models.CharField(max_length=255, blank=True, null=True)
    deleted = models.TextField(blank=True, null=True)  # This field type is a guess.
    modified_by_user = models.CharField(max_length=255, blank=True, null=True)
    class_id = models.BigIntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    discipline = models.IntegerField(blank=True, null=True)
    discipline_description = models.CharField(max_length=255, blank=True, null=True)
    grade = models.IntegerField(blank=True, null=True)
    grade_description = models.CharField(max_length=255, blank=True, null=True)
    presence_state = models.IntegerField(blank=True, null=True)
    student_id = models.BigIntegerField(blank=True, null=True)
    teacher_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'day_point'


class Exam(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_by_user = models.CharField(max_length=255, blank=True, null=True)
    deleted = models.TextField(blank=True, null=True)  # This field type is a guess.
    modified_by_user = models.CharField(max_length=255, blank=True, null=True)
    degree = models.IntegerField(blank=True, null=True)
    exam_date = models.DateTimeField(blank=True, null=True)
    exam_duration = models.IntegerField(blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    teacher_id = models.BigIntegerField(blank=True, null=True)
    lesson = models.ForeignKey('Lesson', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'exam'


class Homework(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_by_user = models.CharField(max_length=255, blank=True, null=True)
    deleted = models.TextField(blank=True, null=True)  # This field type is a guess.
    modified_by_user = models.CharField(max_length=255, blank=True, null=True)
    class_id = models.BigIntegerField(blank=True, null=True)
    description = models.CharField(max_length=2000, blank=True, null=True)
    expire_date = models.DateField(blank=True, null=True)
    file_link = models.CharField(max_length=255, blank=True, null=True)
    lesson_id = models.BigIntegerField(blank=True, null=True)
    send_date = models.DateField(blank=True, null=True)
    state = models.IntegerField(blank=True, null=True)
    student_comment = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'homework'


class Lesson(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_by_user = models.CharField(max_length=255, blank=True, null=True)
    deleted = models.TextField(blank=True, null=True)  # This field type is a guess.
    modified_by_user = models.CharField(max_length=255, blank=True, null=True)
    school_id = models.BigIntegerField(blank=True, null=True)
    code = models.CharField(max_length=255, blank=True, null=True)
    course_unit = models.IntegerField(blank=True, null=True)
    degree = models.IntegerField(blank=True, null=True)
    field = models.IntegerField(blank=True, null=True)
    gender = models.IntegerField(blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    state = models.IntegerField(blank=True, null=True)
    time_in_week = models.IntegerField(blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'lesson'


class MenuItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_by_user = models.CharField(max_length=255, blank=True, null=True)
    deleted = models.TextField(blank=True, null=True)  # This field type is a guess.
    modified_by_user = models.CharField(max_length=255, blank=True, null=True)
    code = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'menu_item'


class Resource(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_by_user = models.CharField(max_length=255, blank=True, null=True)
    deleted = models.TextField(blank=True, null=True)  # This field type is a guess.
    modified_by_user = models.CharField(max_length=255, blank=True, null=True)
    duplicate = models.TextField(blank=True, null=True)  # This field type is a guess.
    duplicate_count = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    path = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    volume = models.BigIntegerField(blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'resource'


class Role(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_by_user = models.CharField(max_length=255, blank=True, null=True)
    deleted = models.TextField(blank=True, null=True)  # This field type is a guess.
    modified_by_user = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'role'


class RoleAcctionsGroup(models.Model):
    role = models.ForeignKey(Role, models.DO_NOTHING)
    acctions_group = models.BigIntegerField(blank=True, null=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        # managed = False
        db_table = 'role_acctions_group'


class RoleMenu(models.Model):
    role = models.ForeignKey(Role, models.DO_NOTHING)
    menu = models.BigIntegerField(blank=True, null=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        # managed = False
        db_table = 'role_menu'


class Schedule(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_by_user = models.CharField(max_length=255, blank=True, null=True)
    deleted = models.TextField(blank=True, null=True)  # This field type is a guess.
    modified_by_user = models.CharField(max_length=255, blank=True, null=True)
    break_duration = models.IntegerField(blank=True, null=True)
    class_id = models.BigIntegerField(blank=True, null=True)
    degree = models.IntegerField(blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
    owner_id = models.BigIntegerField(blank=True, null=True)
    school_id = models.BigIntegerField(blank=True, null=True)
    section_count = models.IntegerField(blank=True, null=True)
    section_duration = models.IntegerField(blank=True, null=True)
    start_time = models.CharField(max_length=255, blank=True, null=True)
    teacher_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'schedule'


class ScheduleSections(models.Model):
    schedule = models.ForeignKey(Schedule, models.DO_NOTHING)
    sections = models.BigIntegerField(blank=True, null=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        # managed = False
        db_table = 'schedule_sections'


class School(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_by_user = models.CharField(max_length=255, blank=True, null=True)
    deleted = models.TextField(blank=True, null=True)  # This field type is a guess.
    modified_by_user = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    code = models.CharField(max_length=255, blank=True, null=True)
    gender = models.IntegerField(blank=True, null=True)
    info_completed = models.TextField(blank=True, null=True)  # This field type is a guess.
    logo = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    office = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'school'


class SchoolDegrees(models.Model):
    school = models.ForeignKey(School, models.DO_NOTHING)
    degrees = models.IntegerField(blank=True, null=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        # managed = False
        db_table = 'school_degrees'


class SchoolLevels(models.Model):
    school = models.ForeignKey(School, models.DO_NOTHING)
    levels = models.IntegerField(blank=True, null=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        # managed = False
        db_table = 'school_levels'


class Section(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_by_user = models.CharField(max_length=255, blank=True, null=True)
    deleted = models.TextField(blank=True, null=True)  # This field type is a guess.
    modified_by_user = models.CharField(max_length=255, blank=True, null=True)
    class_id = models.BigIntegerField(blank=True, null=True)
    class_type = models.IntegerField(blank=True, null=True)
    day_of_week = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=2000, blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    section_order = models.IntegerField(blank=True, null=True)
    selected_lesson = models.BigIntegerField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    teacher_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'section'


class ClassMeeting(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_by_user = models.CharField(max_length=255, blank=True, null=True)
    deleted = models.TextField(blank=True, null=True)  # This field type is a guess.
    modified_by_user = models.CharField(max_length=255, blank=True, null=True)
    class_id = models.ForeignKey('Classroom',on_delete=models.DO_NOTHING, db_column='class_id')
    class_name = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    degree = models.IntegerField(blank=True, null=True)
    ended = models.TextField()  # This field type is a guess.
    ended_time = models.TimeField(blank=True, null=True)
    lesson_name = models.CharField(max_length=255, blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
    school_id = models.BigIntegerField(blank=True, null=True)
    #section_id = models.BigIntegerField(blank=True, null=True)
    section_id = models.ForeignKey('Section',on_delete=models.DO_NOTHING, db_column='section_id')
    started_time = models.TimeField(blank=True, null=True)
    teacher_id = models.BigIntegerField(blank=True, null=True)
    token = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'class_meeting'


class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_by_user = models.CharField(max_length=255, blank=True, null=True)
    deleted = models.TextField(blank=True, null=True)  # This field type is a guess.
    modified_by_user = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    birth_date = models.DateTimeField(blank=True, null=True)
    birth_place = models.CharField(max_length=255, blank=True, null=True)
    cert_code = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    degree = models.IntegerField(blank=True, null=True)
    education_state = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    father_name = models.CharField(max_length=255, blank=True, null=True)
    father_phone = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    gender = models.IntegerField(blank=True, null=True)
    job = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
    mobile_no = models.CharField(max_length=255, blank=True, null=True)
    mother_name = models.CharField(max_length=255, blank=True, null=True)
    mother_phone = models.CharField(max_length=255, blank=True, null=True)
    national_code = models.CharField(unique=True, max_length=255, blank=True, null=True)
    parent_id = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    phone_no = models.CharField(max_length=255, blank=True, null=True)
    profile_completed = models.TextField(blank=True, null=True)  # This field type is a guess.
    profile_image = models.CharField(max_length=255, blank=True, null=True)
    relationship = models.CharField(max_length=255, blank=True, null=True)
    role = models.BigIntegerField(blank=True, null=True)
    school_id = models.BigIntegerField(blank=True, null=True)
    state = models.IntegerField(blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=255, blank=True, null=True)
    field = models.IntegerField(blank=True, null=True)
    birth_certificate_image = models.CharField(max_length=255, blank=True, null=True)
    national_card_image = models.CharField(max_length=255, blank=True, null=True)
    meetings = models.ManyToManyField('ClassMeeting',through='PresenceAbsence', related_name='students', blank=True)

    class Meta:
        # managed = False
        db_table = 'user'
    
    @property
    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)


class Classroom(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_by_user = models.CharField(max_length=255, blank=True, null=True)
    deleted = models.TextField(blank=True, null=True)  # This field type is a guess.
    modified_by_user = models.CharField(max_length=255, blank=True, null=True)
    break_duration = models.IntegerField(blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)
    degree = models.IntegerField(blank=True, null=True)
    field = models.IntegerField(blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    schedule = models.BigIntegerField(blank=True, null=True)
    school_id = models.BigIntegerField(blank=True, null=True)
    section_count = models.IntegerField(blank=True, null=True)
    section_duration = models.IntegerField(blank=True, null=True)
    start_time = models.CharField(max_length=255, blank=True, null=True)
    students = models.ManyToManyField('User',through='ClassroomStudents', related_name='classes', blank=True)

    class Meta:
        # managed = False
        db_table = 'classroom'


class SectionLessons(models.Model):
    section = models.ForeignKey(Section, models.DO_NOTHING)
    lessons = models.BigIntegerField(blank=True, null=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        # managed = False
        db_table = 'section_lessons'


class SmsVerification(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_by_user = models.CharField(max_length=255, blank=True, null=True)
    deleted = models.TextField(blank=True, null=True)  # This field type is a guess.
    modified_by_user = models.CharField(max_length=255, blank=True, null=True)
    code = models.CharField(max_length=255, blank=True, null=True)
    expiration_date = models.BigIntegerField(blank=True, null=True)
    mobile_no = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'sms_verification'


class TimeInterval(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_by_user = models.CharField(max_length=255, blank=True, null=True)
    deleted = models.TextField(blank=True, null=True)  # This field type is a guess.
    modified_by_user = models.CharField(max_length=255, blank=True, null=True)
    class_type = models.IntegerField(blank=True, null=True)
    day_of_week = models.CharField(max_length=255, blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    teacher_id = models.BigIntegerField(blank=True, null=True)
    teacher_timeline_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'time_interval'


class TimeLineFreeTimeIntervals(models.Model):
    time_line = models.ForeignKey('Timeline', models.DO_NOTHING)
    free_time_intervals = models.BigIntegerField(blank=True, null=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        # managed = False
        db_table = 'time_line_free_time_intervals'


class TimeLineLessons(models.Model):
    time_line = models.ForeignKey('Timeline', models.DO_NOTHING)
    lessons = models.BigIntegerField(blank=True, null=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        # managed = False
        db_table = 'time_line_lessons'


class TimeLineReservedTimeIntervals(models.Model):
    time_line = models.ForeignKey('Timeline', models.DO_NOTHING)
    reserved_time_intervals = models.BigIntegerField(blank=True, null=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        # managed = False
        db_table = 'time_line_reserved_time_intervals'


class Timeline(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_by_user = models.CharField(max_length=255, blank=True, null=True)
    deleted = models.TextField(blank=True, null=True)  # This field type is a guess.
    modified_by_user = models.CharField(max_length=255, blank=True, null=True)
    teacher_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'timeline'


class ClassroomStudents(models.Model):
    classroom = models.ForeignKey('Classroom', on_delete=models.SET_NULL, related_name='class_students', blank=True, null=True)
    students = models.ForeignKey('User',on_delete=models.SET_NULL, related_name='class_students', blank=True, null=True, db_column='students')
    class Meta:
        # managed = False
        db_table = 'classroom_students'


class ClassMeetingStudents(models.Model):
    class_meeting = models.ForeignKey(ClassMeeting, models.DO_NOTHING)
    #students = models.BigIntegerField(blank=True, null=True)
    students = models.ForeignKey(User,on_delete=models.DO_NOTHING, db_column='students')
    id = models.BigAutoField(primary_key=True)

    class Meta:
        # managed = False
        db_table = 'class_meeting_students'


class UserImages(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    images = models.CharField(max_length=255, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        # managed = False
        db_table = 'user_images'


class UserMyClassesId(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    my_classes_id = models.BigIntegerField(blank=True, null=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        # managed = False
        db_table = 'user_my_classes_id'


class UserOtherDocumentImages(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    other_document_images = models.CharField(max_length=255, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        # managed = False
        db_table = 'user_other_document_images'


class UserProficiency(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    proficiency = models.CharField(max_length=255, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        # managed = False
        db_table = 'user_proficiency'


class UserResource(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    resource = models.BigIntegerField(blank=True, null=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        # managed = False
        db_table = 'user_resource'


##################################################################################
#                        Added models for django server                          #
##################################################################################


class BaseClass(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class NewExam(BaseClass):
    ONLINE = 'O'
    INPERSON = 'I'
    CLASSTYPE_CHOICES = [
        (ONLINE, 'online'),
        (INPERSON, 'inperson'),
    ]
    id = models.BigAutoField(primary_key=True)
    class_id = models.ForeignKey(Classroom,on_delete=models.DO_NOTHING)
    lesson_id = models.ForeignKey(Lesson,on_delete=models.DO_NOTHING)
    date = models.DateField(auto_now=False, auto_now_add=False)
    time = models.TimeField(auto_now=False, auto_now_add=False)
    duration = models.BigIntegerField()
    class_type = models.CharField(max_length=1,choices=CLASSTYPE_CHOICES)
    done = models.BooleanField(default=False)
    class Meta:
        # managed = False
        db_table = 'new_exam'


class NewExamMeeting(BaseClass):

    exam = models.ForeignKey(NewExam,on_delete=models.DO_NOTHING)
    token = models.CharField(max_length=255, blank=True, null=True)
    students = models.ManyToManyField('User',through='NewExamScore', related_name='exam_meeting', blank=True)
    done = models.BooleanField(default=False)

    class Meta:
        # managed = False
        db_table = 'new_exam_meeting'


# class NewExamMeetingStudents(models.Model):
    
#     exam_meeting = models.ForeignKey(NewExamMeeting, models.DO_NOTHING)
#     students = models.ForeignKey(User,on_delete=models.DO_NOTHING, db_column='students')
    
#     class Meta:
#         # managed = False
#         db_table = 'new_exam_meeting_students'

class NewExamScore(BaseClass):

    quiz = models.ForeignKey('Quizzes',on_delete=models.DO_NOTHING)
    student = models.ForeignKey('User',on_delete=models.DO_NOTHING)
    exam_meeting = models.ForeignKey('NewExamMeeting',on_delete=models.DO_NOTHING)
    score = models.FloatField(blank=True, null=True)
    submitted_choices = models.CharField(max_length=2000, blank=True, null=True)
    score_text = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'new_exam_score'


class NewHomework(BaseClass):
    id = models.BigAutoField(primary_key=True)
    class_id = models.ForeignKey('Classroom', related_name='homeworks',on_delete=models.SET_NULL, null=True)
    lesson_id = models.ForeignKey('Lesson', related_name='homeworks',on_delete=models.SET_NULL,null=True)
    description = models.CharField(max_length=2000, blank=True, null=True)
    file = models.CharField(max_length=255, blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)
    responses = models.ManyToManyField('User',through='NewHomeworkResponse', related_name='homeworks', blank=True)

    class Meta:
        # managed = False
        db_table = 'new_homework'


class NewHomeworkResponse(BaseClass):
    id = models.BigAutoField(primary_key=True)
    homework_id = models.ForeignKey('NewHomework', related_name='homeworks_response', on_delete=models.SET_NULL, null=True)
    student_id = models.ForeignKey('User', related_name='homeworks_response',on_delete=models.SET_NULL, null=True)
    done = models.BooleanField(default=False)
    file = models.CharField(max_length=255, blank=True, null=True)
    submitdate = models.DateTimeField(default=None, null=True, blank=True)
    class Meta:
        # managed = False
        db_table = 'new_homework_response'


class Quizzes(BaseClass):
    QUIZ = 'Q'
    EXAM = 'E'
    EXAMTYPE_CHOICES = [
        (QUIZ, 'quiz'),
        (EXAM, 'exam'),
    ]
    id = models.BigAutoField(primary_key=True)
    teacher_id = models.ForeignKey(User,on_delete=models.DO_NOTHING, related_name='teacher_quiz')
    lesson_id = models.ForeignKey(Lesson,on_delete=models.DO_NOTHING)
    quiz_title = models.CharField(max_length=200, blank=True, null=True)
    quiz_text = models.CharField(max_length=2000, blank=True, null=True)
    # duration = models.DurationField(blank=True, null=True)
    duration = models.BigIntegerField(blank=True, null=True)
    students = models.ManyToManyField('User',through='QuizScore', related_name='quizzes', blank=True)
    quiz_type = models.CharField(max_length=1,choices=EXAMTYPE_CHOICES)

    class Meta:
        # managed = False
        db_table = 'quizzes'


class QuizScore(BaseClass):
    id = models.BigAutoField(primary_key=True)
    quiz = models.ForeignKey('Quizzes',on_delete=models.DO_NOTHING)
    student = models.ForeignKey('User',on_delete=models.DO_NOTHING)
    class_meeting = models.ForeignKey('ClassMeeting',on_delete=models.DO_NOTHING)
    score = models.FloatField(blank=True, null=True)
    submitted_choices = models.CharField(max_length=2000, blank=True, null=True)
    score_text = models.CharField(max_length=200, blank=True, null=True)
    
    class Meta:
        # managed = False
        db_table = 'quiz_score'


class PresenceAbsence(BaseClass):
    ABSENT = 'A'
    ENTRANCE = 'E'
    VERIFIED = 'V'
    END_SET_ABSENT = 'U'
    STATUS_CHOICES = [
        (ABSENT, 'absent'),
        (ENTRANCE, 'entrance'),
        (VERIFIED, 'verified'),
        (END_SET_ABSENT, 'end_set_absent')
    ]
    class_meeting = models.ForeignKey('ClassMeeting', related_name='class_sheet', on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey(User, related_name='class_sheet', on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=ABSENT, blank=False, null=False)
    meeting_score = models.IntegerField(blank=True, null=True)
    has_disciplinary = models.BooleanField(default=False, blank=True, null=False)
    disciplinary = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'class_sheet'


class TeacherAvailability(BaseClass):
    SATURDAY = 1
    SUNDAY = 2
    MONDAY = 3
    TUESDAY = 4
    WEDNESDAY = 5
    THURSDAY = 6
    FRIDAY = 7
    DAY_OF_WEEK_CHOICES = [
        (SATURDAY, 'SATURDAY'),
        (SUNDAY, 'SUNDAY'),
        (MONDAY, 'MONDAY'),
        (TUESDAY, 'TUESDAY'),
        (WEDNESDAY, 'WEDNESDAY'),
        (THURSDAY, 'THURSDAY'),
        (FRIDAY, 'FRIDAY')
    ]

    id = models.BigAutoField(primary_key=True)
    teacher_id = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    day_of_week = models.IntegerField(choices=DAY_OF_WEEK_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    online = models.BooleanField()
    verified = models.BooleanField(default=False)
    class Meta:
        # managed = False
        db_table = 'teacher_availability'


class TeacherLessons(BaseClass):
    id = models.BigAutoField(primary_key=True)
    teacher_id = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    lesson_id = models.ForeignKey(Lesson,on_delete=models.DO_NOTHING)
    class Meta:
        # managed = False
        db_table = 'teacher_lessons'


class MeetingScorePerDay(BaseClass):

    teacher_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='teacher_scores')
    student_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='student_scores')
    lesson_id = models.ForeignKey(Lesson, on_delete=models.DO_NOTHING)
    class_id = models.ForeignKey(Classroom, on_delete=models.DO_NOTHING)
    date = models.DateField(blank=True, null=True)
    score = models.FloatField(blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'meeting_score_per_day'


class DisciplinaryPerDay(BaseClass):

    teacher_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='teacher_notes')
    student_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='student_notes')
    lesson_id = models.ForeignKey(Lesson, on_delete=models.DO_NOTHING)
    class_id = models.ForeignKey(Classroom, on_delete=models.DO_NOTHING)
    date = models.DateField(blank=True, null=True)
    has_disciplinary = models.BooleanField(default=False, blank=True, null=False)
    disciplinary = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'disciplinary_per_day'

class ParentChild(BaseClass):
    
    parent = models.ForeignKey('User',on_delete=models.DO_NOTHING, related_name='children')
    child = models.ForeignKey('User',on_delete=models.DO_NOTHING, related_name='parents')
    
    class Meta:
        # managed = False
        db_table = 'parent_child'

class DiskUsage(BaseClass):

    max_disk_usage = models.IntegerField(default=0)

    class Meta:
        # managed = False
        db_table = 'disk_usage'

class SavedVideos(BaseClass):

    class_meeting = models.ForeignKey(ClassMeeting, on_delete=models.DO_NOTHING, related_name='videos')
    location = models.CharField(max_length=1024, blank=True, null=True)
    disk_usage = models.IntegerField(blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'saved_videos'