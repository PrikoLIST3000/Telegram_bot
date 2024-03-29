from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from aiogram import Router, F
from aiogram.filters import StateFilter
from keyboards.for_quiz import get_start_quiz_kb
from sqlalchemy.ext.asyncio import AsyncSession
from database.orm_query import orm_update_user_quiz_state, orm_is_quiz_completed
from utils.quiz import QuizIterator, AnswersIterator

router = Router()


class Quiz(StatesGroup):
    start_quiz = State()
    q1 = State()
    q2 = State()
    q3 = State()
    q4 = State()
    q5 = State()


@router.message(StateFilter(None), F.text.lower() == 'прохождение теста')
async def send_welcome(message: Message, state: FSMContext, session: AsyncSession):
    check_for_quiz = await orm_is_quiz_completed(session, message.from_user.id)
    if check_for_quiz:
        await message.reply("Ой, ты уже проходил викторину", reply_markup=get_start_quiz_kb())
    else:
        await state.set_state(Quiz.start_quiz)
        await message.reply("Привет! Давай начнем викторину", reply_markup=get_start_quiz_kb())


@router.message(Quiz.start_quiz, F.text.lower() == 'начать')
async def start_quiz(message: Message, state: FSMContext):
    await state.set_state(Quiz.q1)
    quiz = QuizIterator()
    correct_answer = AnswersIterator()
    await state.update_data(quiz=quiz, correct_answer=correct_answer, correct_answers=0)
    await message.reply(next(quiz))


@router.message(Quiz.q1)
async def answer_q1(message: Message, state: FSMContext):
    data = await state.get_data()
    if message.text == next(data['correct_answer']):
        await state.update_data(correct_answers=data['correct_answers'] + 1)
    await state.set_state(Quiz.q2)
    await message.reply(next(data['quiz']))


@router.message(Quiz.q2)
async def answer_q2(message: Message, state: FSMContext):
    data = await state.get_data()
    if message.text == next(data['correct_answer']):
        await state.update_data(correct_answers=data['correct_answers'] + 1)
    await state.set_state(Quiz.q3)
    await message.reply(next(data['quiz']))


@router.message(Quiz.q3)
async def answer_q3(message: Message, state: FSMContext):
    data = await state.get_data()
    if message.text == next(data['correct_answer']):
        await state.update_data(correct_answers=data['correct_answers'] + 1)
    await state.set_state(Quiz.q4)
    await message.reply(next(data['quiz']))


@router.message(Quiz.q4)
async def answer_q4(message: Message, state: FSMContext):
    data = await state.get_data()
    if message.text == next(data['correct_answer']):
        await state.update_data(correct_answers=data['correct_answers'] + 1)
    await state.set_state(Quiz.q5)
    await message.reply(next(data['quiz']))


@router.message(Quiz.q5)
async def answer_q5(message: Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    if message.text == next(data['correct_answer']):
        await state.update_data(correct_answers=data['correct_answers'] + 1)
    data = await state.get_data()
    await message.reply(f"Поздравляем! Вы дали {data['correct_answers']} правильных ответов из 5.")
    await orm_update_user_quiz_state(session, message.from_user.id)
    await state.clear()
