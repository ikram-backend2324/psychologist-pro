from modeltranslation.translator import TranslationOptions, register

from .models import Category, QuizQuestion, Step, Topic


@register(Category)
class CategoryTR(TranslationOptions):
    fields = ("name",)


@register(Topic)
class TopicTR(TranslationOptions):
    fields = ("title", "summary", "description", "goal")


@register(Step)
class StepTR(TranslationOptions):
    fields = ("title", "body", "result_low", "result_mid", "result_high")


@register(QuizQuestion)
class QuizQuestionTR(TranslationOptions):
    fields = ("text", "options")
