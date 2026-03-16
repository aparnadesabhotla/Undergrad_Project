from django.contrib.auth import mixins
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.urls import reverse
from blog import models as blog_models


def permission_denied(request):
    context = request.session['permission_denied']
    template = 'blog/permission_denied.html'
    return render(request, template, context)


def index(request):
    questions_list = blog_models.Question.objects.order_by('-published')
    context = {
        'questions_list': questions_list
    }
    template = 'blog/index.html'
    return render(request, template, context)


def detail(request, question_id):
    question = get_object_or_404(blog_models.Question, pk=question_id)
    answers = question.answer_set.order_by('-published').all()
    context = {
        'question': question,
        'answers': answers
    }
    template = 'blog/detail.html'
    return render(request, template, context)


class QuestionAskView(mixins.LoginRequiredMixin, generic.CreateView):
    model = blog_models.Question
    template_name = 'blog/question_ask.html'
    fields = ['title', 'body']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question_ask_edit_form'] = context.pop('form')
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        context = {'question_id': self.object.id}
        return reverse('blog:question-detail', kwargs=context)


class QuestionEditView(mixins.UserPassesTestMixin, generic.UpdateView):
    model = blog_models.Question
    template_name = 'blog/question_edit.html'
    pk_url_kwarg = 'question_id'
    fields = ['title', 'body']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question_ask_edit_form'] = context.pop('form')
        context['question'] = context.pop('object')
        return context

    def get_success_url(self):
        context = {'question_id': self.object.id}
        return reverse('blog:question-detail', kwargs=context)

    def test_func(self):
        question = self.get_object()
        if self.request.user == question.author:
            return True
        return False

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            self.request.session['permission_denied'] = {'model': 'question', 'operation': 'edit'}
            return redirect('blog:permission-denied')
        else:
            redirect_url = f"{reverse('user:login')}?next={self.request.path}"
            return redirect(redirect_url)


class QuestionDeleteView(mixins.UserPassesTestMixin, generic.DeleteView):
    model = blog_models.Question
    template_name = 'blog/question_delete.html'
    pk_url_kwarg = 'question_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question_delete_form'] = context.pop('form')
        context['question'] = context.pop('object')
        return context

    def get_success_url(self):
        return reverse('blog:question-index')

    def test_func(self):
        question = self.get_object()
        if self.request.user == question.author:
            return True
        return False

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            self.request.session['permission_denied'] = {'model': 'question', 'operation': 'delete'}
            return redirect('blog:permission-denied')
        else:
            redirect_url = f"{reverse('user:login')}?next={self.request.path}"
            return redirect(redirect_url)

    
class AnswerAddView(mixins.LoginRequiredMixin, generic.CreateView):
    model = blog_models.Answer
    template_name = 'blog/answer_add.html'
    pk_url_kwarg = 'question_id'
    fields = ['body']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['answer_add_form'] = context.pop('form')
        question = get_object_or_404(blog_models.Question, pk=self.kwargs.get('question_id'))
        answers = question.answer_set.order_by('-published').all()
        context.update({'question': question, 'answers': answers})
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.question = get_object_or_404(blog_models.Question, pk=self.kwargs.get('question_id'))
        return super().form_valid(form)

    def get_success_url(self):
        context = {'question_id': self.kwargs.get('question_id')}
        return reverse('blog:question-detail', kwargs=context)


class AnswerEditView(mixins.UserPassesTestMixin, generic.UpdateView):
    model = blog_models.Answer
    template_name = 'blog/answer_edit.html'
    pk_url_kwarg = 'answer_id'
    fields = ['body']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['answer_edit_form'] = context.pop('form')
        question = get_object_or_404(blog_models.Question, pk=self.kwargs.get('question_id'))
        answers = question.answer_set.order_by('-published').all()
        context.update({'question': question, 'answers': answers, 'answer_selected': self.get_object()})
        return context

    def get_success_url(self):
        context = {'question_id': self.kwargs.get('question_id')}
        return reverse('blog:question-detail', kwargs=context)

    def test_func(self):
        answer = self.get_object()
        if self.request.user == answer.author:
            return True
        return False

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            self.request.session['permission_denied'] = {'model': 'answer', 'operation': 'edit'}
            return redirect('blog:permission-denied')
        else:
            redirect_url = f"{reverse('user:login')}?next={self.request.path}"
            return redirect(redirect_url)


class AnswerDeleteView(mixins.UserPassesTestMixin, generic.DeleteView):
    model = blog_models.Answer
    template_name = 'blog/answer_delete.html'
    pk_url_kwarg = 'answer_id'
    fields = ['body']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['answer_delete_form'] = context.pop('form')
        question = get_object_or_404(blog_models.Question, pk=self.kwargs.get('question_id'))
        answers = question.answer_set.order_by('-published').all()
        context.update({'question': question, 'answers': answers, 'answer_selected': self.get_object()})
        return context
    
    def get_success_url(self):
        context = {'question_id': self.kwargs.get('question_id')}
        return reverse('blog:question-detail', kwargs=context)

    def test_func(self):
        answer = self.get_object()
        if self.request.user == answer.author:
            return True
        return False

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            self.request.session['permission_denied'] = {'model': 'answer', 'operation': 'delete'}
            return redirect('blog:permission-denied')
        else:
            redirect_url = f"{reverse('user:login')}?next={self.request.path}"
            return redirect(redirect_url)
