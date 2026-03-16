from django.urls import path
from blog import views as blog_views

app_name = 'blog'
urlpatterns = [
    path('', blog_views.index, name='question-index'),
    path('permission_denied/', blog_views.permission_denied, name='permission-denied'),
    path('question/ask', blog_views.QuestionAskView.as_view(), name='question-ask'),
    path('question/<int:question_id>/detail', blog_views.detail, name='question-detail'),
    path('question/<int:question_id>/edit', blog_views.QuestionEditView.as_view(), name='question-edit'),
    path('question/<int:question_id>/delete', blog_views.QuestionDeleteView.as_view(), name='question-delete'),
    path('question/<int:question_id>/answer/add', blog_views.AnswerAddView.as_view(), name='answer-add'),
    path('question/<int:question_id>/answer/<int:answer_id>/edit', blog_views.AnswerEditView.as_view(), name='answer-edit'),
    path('question/<int:question_id>/answer/<int:answer_id>/delete', blog_views.AnswerDeleteView.as_view(), name='answer-delete'),
]
