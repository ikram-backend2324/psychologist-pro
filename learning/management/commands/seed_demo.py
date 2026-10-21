"""Idempotent demo content in Uzbek, Karakalpak, Russian and English."""
from django.core.management.base import BaseCommand
from django.db import transaction

from accounts.admin import PSYCHOLOGIST_GROUP
from accounts.models import User
from learning.demo_content import EXTRA_CATEGORIES, EXTRA_PSYCHOLOGISTS, EXTRA_TOPICS, PROFILE_DEFAULTS
from learning.models import Category, QuizQuestion, Step, Topic

LANGS = ("uz", "kaa", "ru", "en")


def tr(obj, field, values):
    """values: (uz, kaa, ru, en)."""
    for lang, value in zip(LANGS, values):
        setattr(obj, f"{field}_{lang}", value)


CATEGORIES = [
    ("communication", "💬", "ocean", ("Muloqot", "Qarım-qatnas", "Общение", "Communication")),
    ("stress", "🌿", "mint", ("Stress va xotirjamlik", "Stress hám tınıshlıq", "Стресс и спокойствие", "Stress & calm")),
    ("confidence", "🦋", "violet", ("O‘ziga ishonch", "Ózine isenim", "Уверенность в себе", "Self-confidence")),
    ("relationships", "🏡", "rose", ("Oila va munosabatlar", "Shańaraq hám qatnaslar", "Семья и отношения", "Family & relationships")),
]

PSYCHOLOGISTS = [
    {
        "username": "dilnoza.karimova",
        "first_name": "Dilnoza",
        "last_name": "Karimova",
        "specialization": "Kommunikativ psixologiya",
        "experience_years": 9,
        "bio": "Muloqot ko‘nikmalari va o‘ziga ishonchni rivojlantirish bo‘yicha mutaxassis.",
    },
    {
        "username": "aziz.rahimov",
        "first_name": "Aziz",
        "last_name": "Rahimov",
        "specialization": "Klinik psixolog, stress terapiyasi",
        "experience_years": 12,
        "bio": "Stress, xavotir va hissiy charchoq bilan ishlaydi.",
    },
]

FREQ_OPTIONS = (
    "Hech qachon | 0\nBa’zan | 1\nKo‘pincha | 2\nDoim | 3",
    "Hesh qashan | 0\nGeyde | 1\nKóbinese | 2\nÁrqashan | 3",
    "Никогда | 0\nИногда | 1\nЧасто | 2\nВсегда | 3",
    "Never | 0\nSometimes | 1\nOften | 2\nAlways | 3",
)
FREQ_OPTIONS_REVERSED = (
    "Hech qachon | 3\nBa’zan | 2\nKo‘pincha | 1\nDoim | 0",
    "Hesh qashan | 3\nGeyde | 2\nKóbinese | 1\nÁrqashan | 0",
    "Никогда | 3\nИногда | 2\nЧасто | 1\nВсегда | 0",
    "Never | 3\nSometimes | 2\nOften | 1\nAlways | 0",
)

TOPICS = [
    {
        "slug": "how-to-communicate-with-people",
        "category": "communication",
        "author": "dilnoza.karimova",
        "icon": "🗣️",
        "color": "ocean",
        "level": "beginner",
        "minutes": 20,
        "tags": "communication, listening, confidence",
        "title": ("Odamlar bilan qanday muloqot qilish kerak", "Adamlar menen qalay sóylesiw kerek", "Как общаться с людьми", "How to communicate with people"),
        "summary": (
            "Faol tinglash, aniq gapirish va ishonchli muloqotning amaliy sirlari.",
            "Belsendi tıńlaw, anıq sóylew hám isenimli qarım-qatnastıń ámeliy sırları.",
            "Практические секреты активного слушания, ясной речи и уверенного общения.",
            "Practical secrets of active listening, clear speech and confident conversation.",
        ),
        "goal": (
            "Suhbatdoshingizni tinglash va o‘z fikringizni xotirjam ifodalashni o‘rganasiz.",
            "Sóylesiwshińizdi tıńlawdı hám óz pikirińizdi tınısh bildiriwdi úyrenesiz.",
            "Вы научитесь слушать собеседника и спокойно выражать свои мысли.",
            "You will learn to listen to others and express your thoughts calmly.",
        ),
        "description": (
            "Muloqot — bu o‘rganish mumkin bo‘lgan ko‘nikma. Ushbu mavzuda qisqa dars, test, o‘yin kartalari va mulohaza savoli bor.",
            "Qarım-qatnas — úyreniwge bolatuǵın kónlikpe. Bul temada qısqa sabaq, test, oyın kartaları hám oylanıw sorawı bar.",
            "Общение — это навык, которому можно научиться. В теме есть короткий урок, тест, игровые карточки и вопрос для размышления.",
            "Communication is a skill you can learn. This topic has a short lesson, a test, game cards and a reflection question.",
        ),
        "steps": [
            {
                "kind": "lesson",
                "title": ("Faol tinglash nima?", "Belsendi tıńlaw degen ne?", "Что такое активное слушание?", "What is active listening?"),
                "body": (
                    "Ko‘pchilik javob berish uchun tinglaydi, tushunish uchun emas. Faol tinglash — suhbatdoshga to‘liq e’tibor berish.\n\nUch oddiy qadam: ko‘zga qarang, gapni bo‘lmang, eshitganingizni o‘z so‘zlaringiz bilan qaytaring: «Demak, siz ... demoqchisiz».\n\nBu odamga uni tushunishganini his qildiradi va nizolarni kamaytiradi.",
                    "Kópshilik juwap beriw ushın tıńlaydı, túsiniw ushın emes. Belsendi tıńlaw — sóylesiwshige tolıq dıqqat qaratıw.\n\nÚsh ápiwayı qádem: kózge qarań, sózdi bólmeń, esitkenińizdi óz sózlerińiz benen qaytalań: «Demek, siz ... demekshisiz».\n\nBul adamǵa onı túsingenin sezdiredi hám kelispewshilikti azaytadı.",
                    "Большинство слушает, чтобы ответить, а не чтобы понять. Активное слушание — это полное внимание к собеседнику.\n\nТри простых шага: смотрите в глаза, не перебивайте, перескажите услышанное своими словами: «То есть вы хотите сказать...».\n\nТак человек чувствует, что его поняли, и конфликтов становится меньше.",
                    "Most people listen to reply, not to understand. Active listening means giving the other person your full attention.\n\nThree simple steps: keep eye contact, don't interrupt, and repeat what you heard in your own words: “So you mean...”.\n\nThis makes people feel understood and reduces conflict.",
                ),
            },
            {
                "kind": "quiz",
                "title": ("Test: Muloqot ko‘nikmalarim", "Test: Qarım-qatnas kónlikpelerim", "Тест: мои навыки общения", "Test: my communication skills"),
                "body": (
                    "Har bir savolga o‘zingizga eng mos javobni tanlang.",
                    "Hár bir sorawǵa ózińizge eń say juwaptı tańlań.",
                    "Выберите ответ, который больше всего подходит вам.",
                    "Choose the answer that fits you best.",
                ),
                "results": (
                    (
                        "Muloqotda hali qiyinchiliklar bor — bu normal. Har kuni bitta suhbatda faol tinglashni mashq qiling.",
                        "Qarım-qatnasta ele qıyınshılıqlar bar — bul qalıptı jaǵday. Hár kúni bir sáwbette belsendi tıńlawdı shınıqtırıń.",
                        "В общении пока есть трудности — это нормально. Тренируйте активное слушание хотя бы в одном разговоре в день.",
                        "Communication is still a challenge — that's normal. Practise active listening in at least one conversation a day.",
                    ),
                    (
                        "Sizda yaxshi asos bor. Endi nizoli vaziyatlarda ham xotirjam qolishni mashq qiling.",
                        "Sizde jaqsı tiykar bar. Endi kelispewshilik jaǵdaylarında da tınısh qalıwdı shınıqtırıń.",
                        "У вас хорошая база. Теперь тренируйтесь сохранять спокойствие и в конфликтных ситуациях.",
                        "You have a solid base. Now practise staying calm in tense situations too.",
                    ),
                    (
                        "Ajoyib! Siz yaxshi tinglovchisiz. Ko‘nikmalaringizni boshqalarga ham o‘rgating.",
                        "Ájayıp! Siz jaqsı tıńlawshısız. Kónlikpelerińizdi basqalarǵa da úyretiń.",
                        "Отлично! Вы хороший слушатель. Делитесь своими навыками с другими.",
                        "Excellent! You are a great listener. Share your skills with others.",
                    ),
                ),
                "questions": [
                    (("Suhbatdoshning gapini oxirigacha tinglayman.", "Sóylesiwshiniń sózin aqırına shekem tıńlayman.", "Я дослушиваю собеседника до конца.", "I listen to the other person until they finish."), FREQ_OPTIONS),
                    (("Suhbat paytida telefonimga qarayman.", "Sáwbet waqtında telefonıma qarayman.", "Во время разговора я смотрю в телефон.", "I look at my phone during conversations."), FREQ_OPTIONS_REVERSED),
                    (("Tushunmasam, aniqlashtiruvchi savol beraman.", "Túsinbesem, anıqlawshı soraw beremen.", "Если не понял, задаю уточняющий вопрос.", "If I don't understand, I ask a clarifying question."), FREQ_OPTIONS),
                    (("Bahs paytida ovozimni ko‘taraman.", "Tartıs waqtında dawısımdı kóteremen.", "Во время спора я повышаю голос.", "I raise my voice during arguments."), FREQ_OPTIONS_REVERSED),
                ],
            },
            {
                "kind": "cards",
                "title": ("O‘yin: To‘g‘ri iboralar", "Oyın: Durıs sóz dizbekleri", "Игра: правильные фразы", "Game: the right phrases"),
                "body": (
                    "«Sen doim...» | «Men ... paytida xafa bo‘ldim» deb ayting\n«Bu bema’nilik» | «Men boshqacha o‘ylayman, chunki...»\n«Tezroq gapir» | «Shoshilmang, men tinglayapman»\n«Bilaman» | «Qiziq, batafsilroq aytib bering»",
                    "«Sen árqashan...» | «Men ... waqtında renjidim» dep aytıń\n«Bul bos gáp» | «Men basqasha oylayman, sebebi...»\n«Tezirek sóyle» | «Asıqpań, men tıńlap atırman»\n«Bilemen» | «Qızıq, tolıǵıraq aytıp beriń»",
                    "«Ты всегда...» | Скажите: «Я расстроился, когда...»\n«Это ерунда» | «Я думаю иначе, потому что...»\n«Говори быстрее» | «Не спешите, я слушаю»\n«Я знаю» | «Интересно, расскажите подробнее»",
                    "“You always...” | Say: “I felt upset when...”\n“That's nonsense” | “I see it differently, because...”\n“Speak faster” | “Take your time, I'm listening”\n“I know” | “Interesting, tell me more”",
                ),
            },
            {
                "kind": "reflection",
                "title": ("Mulohaza", "Oylanıw", "Размышление", "Reflection"),
                "body": (
                    "Yaqinda kim bilan suhbatingiz yaxshi o‘tmadi? Endi faol tinglash orqali uni qanday boshqacha qilgan bo‘lardingiz?",
                    "Jaqında kim menen sáwbetińiz jaqsı ótpedi? Endi belsendi tıńlaw arqalı onı qalay basqasha qılǵan bolar edińiz?",
                    "С кем недавно у вас не сложился разговор? Как бы вы провели его иначе, используя активное слушание?",
                    "Recently, which conversation didn't go well? How would you do it differently using active listening?",
                ),
            },
        ],
    },
    {
        "slug": "calm-in-ten-minutes",
        "category": "stress",
        "author": "aziz.rahimov",
        "icon": "🌬️",
        "color": "mint",
        "level": "beginner",
        "minutes": 10,
        "tags": "stress, breathing, calm, anxiety",
        "title": ("10 daqiqada xotirjamlik", "10 minutta tınıshlıq", "Спокойствие за 10 минут", "Calm in 10 minutes"),
        "summary": (
            "Stressni tez kamaytiradigan nafas mashqi va o‘z holatingizni baholash testi.",
            "Stressti tez azaytatuǵın dem alıw shınıǵıwı hám óz jaǵdayıńızdı bahalaw testi.",
            "Дыхательная практика, быстро снижающая стресс, и тест на оценку состояния.",
            "A breathing practice that quickly reduces stress, plus a self-check test.",
        ),
        "goal": (
            "Har qanday vaziyatda o‘zingizni tinchlantiradigan oddiy usulni bilib olasiz.",
            "Hár qanday jaǵdayda ózińizdi tınıshlandıratuǵın ápiwayı usıldı bilip alasız.",
            "Вы освоите простой способ успокоиться в любой ситуации.",
            "You will master a simple way to calm down in any situation.",
        ),
        "description": (
            "Stress — organizmning tabiiy javobi. Uni boshqarishni o‘rgansa bo‘ladi.",
            "Stress — organizmniń tábiyiy juwabı. Onı basqarıwdı úyreniwge boladı.",
            "Стресс — естественная реакция организма. Им можно научиться управлять.",
            "Stress is the body's natural response. You can learn to manage it.",
        ),
        "steps": [
            {
                "kind": "lesson",
                "title": ("Stress qanday ishlaydi", "Stress qalay isleydi", "Как работает стресс", "How stress works"),
                "body": (
                    "Xavf sezilganda tana «jang yoki qoch» rejimiga o‘tadi: yurak tez uradi, nafas qisqaradi.\n\nSekin va chuqur nafas miyaga «xavf yo‘q» degan signal yuboradi. Ayniqsa nafas chiqarish nafas olishdan uzunroq bo‘lsa, tana tinchlanadi.",
                    "Qáwip sezilgende dene «gúresiw yamasa qashıw» rejimine ótedi: júrek tez soǵadı, dem alıw tezlesedi.\n\nÁste hám tereń dem alıw miyge «qáwip joq» degen signal jiberedi. Ásirese dem shıǵarıw dem alıwdan uzınıraq bolsa, dene tınıshlanadı.",
                    "При ощущении опасности тело переходит в режим «бей или беги»: сердце бьётся чаще, дыхание становится поверхностным.\n\nМедленное глубокое дыхание посылает мозгу сигнал «опасности нет». Особенно если выдох длиннее вдоха.",
                    "When we sense danger, the body switches to “fight or flight”: the heart races and breathing gets shallow.\n\nSlow, deep breathing tells the brain “there is no danger”, especially when the exhale is longer than the inhale.",
                ),
            },
            {
                "kind": "breathing",
                "title": ("O‘yin: Nafas doirasi", "Oyın: Dem sheńberi", "Игра: дыхательный круг", "Game: the breathing circle"),
                "body": (
                    "Doira kattalashganda nafas oling, kichrayganda chiqaring.",
                    "Sheńber úlkeygende dem alıń, kishireygende shıǵarıń.",
                    "Вдыхайте, когда круг растёт, и выдыхайте, когда он уменьшается.",
                    "Breathe in as the circle grows and out as it shrinks.",
                ),
                "breathing": (4, 4, 6, 4),
            },
            {
                "kind": "quiz",
                "title": ("Test: Stress darajam", "Test: Stress dárejem", "Тест: мой уровень стресса", "Test: my stress level"),
                "body": ("Oxirgi bir hafta haqida o‘ylang.", "Aqırǵı bir hápte haqqında oylań.", "Подумайте о последней неделе.", "Think about the last week."),
                "results": (
                    (
                        "Stress darajangiz yuqori. Har kuni nafas mashqini bajaring va psixolog bilan gaplashishni o‘ylab ko‘ring.",
                        "Stress dárejeńiz joqarı. Hár kúni dem shınıǵıwın orınlań hám psixolog penen sóylesiwdi oylap kóriń.",
                        "Уровень стресса высокий. Делайте дыхательную практику ежедневно и подумайте о разговоре с психологом.",
                        "Your stress level is high. Do the breathing practice daily and consider talking to a psychologist.",
                    ),
                    (
                        "O‘rtacha stress. Dam olish va uyquga ko‘proq e’tibor bering.",
                        "Ortasha stress. Dem alıw hám uyqıǵa kóbirek dıqqat qaratıń.",
                        "Средний уровень стресса. Уделяйте больше внимания отдыху и сну.",
                        "Moderate stress. Pay more attention to rest and sleep.",
                    ),
                    (
                        "Siz stressni yaxshi boshqaryapsiz. Shu odatlaringizni saqlang!",
                        "Siz stressti jaqsı basqarıp atırsız. Usı ádetlerińizdi saqlań!",
                        "Вы хорошо справляетесь со стрессом. Сохраняйте эти привычки!",
                        "You manage stress well. Keep these habits!",
                    ),
                ),
                "questions": [
                    (("Yaxshi uxlay olaman.", "Jaqsı uyıqlay alaman.", "Я хорошо сплю.", "I sleep well."), FREQ_OPTIONS),
                    (("Mayda narsalardan asabiylashaman.", "Mayda nárselerden ashıwlanaman.", "Я раздражаюсь из-за мелочей.", "Small things irritate me."), FREQ_OPTIONS_REVERSED),
                    (("O‘zim uchun dam olishga vaqt topaman.", "Ózim ushın dem alıwǵa waqıt tabaman.", "Я нахожу время на отдых для себя.", "I find time to rest for myself."), FREQ_OPTIONS),
                ],
            },
            {
                "kind": "reflection",
                "title": ("Mulohaza", "Oylanıw", "Размышление", "Reflection"),
                "body": (
                    "Sizni eng ko‘p nima stressga soladi va bu hafta qaysi kichik qadamni qo‘ya olasiz?",
                    "Sizdi eń kóp ne stresske saladı hám bul hápte qaysı kishi qádemdi qoya alasız?",
                    "Что вызывает у вас больше всего стресса и какой маленький шаг вы можете сделать на этой неделе?",
                    "What stresses you most, and what small step can you take this week?",
                ),
            },
        ],
    },
    {
        "slug": "believe-in-yourself",
        "category": "confidence",
        "author": "dilnoza.karimova",
        "icon": "🦋",
        "color": "violet",
        "level": "intermediate",
        "minutes": 15,
        "tags": "confidence, self-esteem, communication",
        "title": ("O‘zingizga ishoning", "Ózińizge iseniń", "Поверь в себя", "Believe in yourself"),
        "summary": (
            "Ichki tanqidchini tinchlantirish va o‘ziga ishonchni oshirish mashqlari.",
            "Ishki sınshını tınıshlandırıw hám ózine isenimdi asırıw shınıǵıwları.",
            "Упражнения, чтобы успокоить внутреннего критика и укрепить уверенность.",
            "Exercises to quiet your inner critic and build confidence.",
        ),
        "goal": (
            "O‘z kuchli tomonlaringizni ko‘rishni va ularga tayanishni o‘rganasiz.",
            "Óz kúshli táreplerińizdi kóriwdi hám olarǵa súyeniwdi úyrenesiz.",
            "Вы научитесь замечать свои сильные стороны и опираться на них.",
            "You will learn to notice your strengths and rely on them.",
        ),
        "description": ("", "", "", ""),
        "steps": [
            {
                "kind": "lesson",
                "title": ("Ichki tanqidchi", "Ishki sınshı", "Внутренний критик", "The inner critic"),
                "body": (
                    "Har birimizda «sen uddalay olmaysan» deydigan ichki ovoz bor. U bizni himoya qilmoqchi, lekin ko‘pincha xalaqit beradi.\n\nUni payqang, nom bering va yaqin do‘stingizga qanday gapirsangiz, o‘zingizga ham shunday gapiring.",
                    "Hár birimizde «sen eplemeyseń» deytuǵın ishki dawıs bar. Ol bizdi qorǵawdı qáleydi, biraq kóbinese kesent beredi.\n\nOnı ańlań, at qoyıń hám jaqın dostıńızǵa qalay sóyleseńiz, ózińizge de solay sóyleń.",
                    "У каждого есть внутренний голос, который говорит «у тебя не получится». Он хочет защитить, но чаще мешает.\n\nЗаметьте его, дайте ему имя и говорите с собой так, как говорили бы с близким другом.",
                    "Everyone has an inner voice saying “you can't do it”. It tries to protect us but often gets in the way.\n\nNotice it, name it, and talk to yourself the way you would talk to a close friend.",
                ),
            },
            {
                "kind": "cards",
                "title": ("O‘yin: Tasdiqlovchi kartalar", "Oyın: Bekkemlewshi kartalar", "Игра: карточки поддержки", "Game: affirmation cards"),
                "body": (
                    "Men xato qildim | Xato — o‘sishning bir qismi\nMen yetarli emasman | Men har kuni o‘rganyapman\nHamma mendan yaxshi | Mening yo‘lim — o‘zimniki\nQo‘rqyapman | Qo‘rquv — yangi narsa boshlanayotganining belgisi",
                    "Men qáte jiberdim | Qáte — ósiwdiń bir bólegi\nMen jetkiliksiz emespen | Men hár kúni úyrenip atırman\nHámme mennen jaqsı | Meniń jolım — óz jolım\nQorqıp atırman | Qorqıw — jańa nárseniń baslanıp atırǵanınıń belgisi",
                    "Я ошибся | Ошибка — часть роста\nЯ недостаточно хорош | Я учусь каждый день\nВсе лучше меня | Мой путь — только мой\nМне страшно | Страх — знак того, что начинается что-то новое",
                    "I made a mistake | Mistakes are part of growth\nI'm not good enough | I am learning every day\nEveryone is better than me | My path is my own\nI'm scared | Fear means something new is starting",
                ),
            },
            {
                "kind": "quiz",
                "title": ("Test: O‘ziga ishonch", "Test: Ózine isenim", "Тест: уверенность в себе", "Test: self-confidence"),
                "body": ("", "", "", ""),
                "results": (
                    (
                        "Ichki tanqidchingiz kuchli. Har kuni bitta yutug‘ingizni yozib boring.",
                        "Ishki sınshıńız kúshli. Hár kúni bir jetiskenligińizdi jazıp barıń.",
                        "Ваш внутренний критик силён. Каждый день записывайте одно своё достижение.",
                        "Your inner critic is strong. Write down one achievement every day.",
                    ),
                    (
                        "Ishonchingiz o‘sib bormoqda. Kichik tavakkallarni davom ettiring.",
                        "Isenimińiz ósip barmaqta. Kishi batıl qádemlerdi dawam ettiriń.",
                        "Уверенность растёт. Продолжайте делать маленькие смелые шаги.",
                        "Your confidence is growing. Keep taking small brave steps.",
                    ),
                    (
                        "Siz o‘zingizga yaxshi ishonasiz — buni boshqalarni qo‘llab-quvvatlashda ham ishlating.",
                        "Siz ózińizge jaqsı isenesiz — bunı basqalardı qollap-quwatlawda da paydalanıń.",
                        "Вы уверены в себе — используйте это, чтобы поддерживать других.",
                        "You trust yourself — use it to support others too.",
                    ),
                ),
                "questions": [
                    (("Yangi ishni boshlashdan qo‘rqmayman.", "Jańa isti baslawdan qorıqpayman.", "Я не боюсь начинать новое.", "I am not afraid to start something new."), FREQ_OPTIONS),
                    (("Xatolarim uchun o‘zimni uzoq ayblayman.", "Qátelerim ushın ózimdi uzaq ayıplayman.", "Я долго виню себя за ошибки.", "I blame myself for mistakes for a long time."), FREQ_OPTIONS_REVERSED),
                    (("Fikrimni ochiq ayta olaman.", "Pikirimdi ashıq ayta alaman.", "Я могу открыто высказать мнение.", "I can openly share my opinion."), FREQ_OPTIONS),
                ],
            },
            {
                "kind": "reflection",
                "title": ("Mulohaza", "Oylanıw", "Размышление", "Reflection"),
                "body": (
                    "O‘zingizdagi uchta kuchli tomonni yozing. Ular sizga qachon yordam bergan?",
                    "Ózińizdegi úsh kúshli tárepti jazıń. Olar sizge qashan járdem bergen?",
                    "Напишите три свои сильные стороны. Когда они вам помогали?",
                    "Write down three of your strengths. When have they helped you?",
                ),
            },
        ],
    },
    {
        "slug": "fear-of-public-speaking",
        "category": "communication",
        "author": "aziz.rahimov",
        "icon": "🎤",
        "color": "sunset",
        "level": "intermediate",
        "minutes": 12,
        "tags": "communication, anxiety, confidence, breathing",
        "title": ("Omma oldida gapirish qo‘rquvi", "Kópshilik aldında sóylew qorqıwı", "Страх публичных выступлений", "Fear of public speaking"),
        "summary": (
            "Chiqishdan oldingi hayajonni boshqarish uchun qisqa reja.",
            "Shıǵıp sóylewden aldınǵı tolqınlanıwdı basqarıw ushın qısqa joba.",
            "Короткий план, как справиться с волнением перед выступлением.",
            "A short plan for handling nerves before you speak.",
        ),
        "goal": (
            "Hayajonni energiyaga aylantirishni o‘rganasiz.",
            "Tolqınlanıwdı energiyaǵa aylandırıwdı úyrenesiz.",
            "Вы научитесь превращать волнение в энергию.",
            "You will learn to turn nerves into energy.",
        ),
        "description": ("", "", "", ""),
        "steps": [
            {
                "kind": "lesson",
                "title": ("Hayajon — dushman emas", "Tolqınlanıw — dushpan emes", "Волнение — не враг", "Nerves are not the enemy"),
                "body": (
                    "Chiqish oldidan yurak tez urishi normal. Bu tana sizni muhim ishga tayyorlayapti.\n\nO‘zingizga «Men qo‘rqyapman» o‘rniga «Men hayajondaman va tayyorman» deng. Bu oddiy almashtirish natijani yaxshilaydi.",
                    "Shıǵıp sóylewden aldın júrektiń tez soǵıwı qalıptı. Bul dene sizdi áhmiyetli iske tayarlap atır.\n\nÓzińizge «Men qorqıp atırman» ornına «Men tolqınlanıp atırman hám tayarman» deń.",
                    "Учащённое сердцебиение перед выступлением — это нормально. Тело готовит вас к важному делу.\n\nСкажите себе не «мне страшно», а «я волнуюсь и готов». Эта простая замена улучшает результат.",
                    "A racing heart before speaking is normal. Your body is preparing you for something important.\n\nInstead of “I'm scared”, tell yourself “I'm excited and ready”. This simple swap improves results.",
                ),
            },
            {
                "kind": "breathing",
                "title": ("Chiqishdan oldin nafas", "Shıǵıp sóylewden aldın dem alıw", "Дыхание перед выступлением", "Breathing before you speak"),
                "body": ("", "", "", ""),
                "breathing": (4, 2, 6, 3),
            },
            {
                "kind": "reflection",
                "title": ("Mulohaza", "Oylanıw", "Размышление", "Reflection"),
                "body": (
                    "Keyingi chiqishingizni tasavvur qiling. Qaysi lahza eng qo‘rqinchli va unga qanday tayyorlanasiz?",
                    "Keyingi shıǵıwıńızdı kóz aldıńızǵa keltiriń. Qaysı waqıt eń qorqınıshlı hám oǵan qalay tayarlanasız?",
                    "Представьте своё следующее выступление. Какой момент самый страшный и как вы к нему подготовитесь?",
                    "Imagine your next talk. Which moment feels scariest, and how will you prepare for it?",
                ),
            },
        ],
    },
]


class Command(BaseCommand):
    help = "Create demo categories, psychologists and topics (safe to run repeatedly)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--refresh",
            action="store_true",
            help="Also rewrite the texts of demo topics that already exist (e.g. after translation fixes).",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        from django.contrib.auth.models import Group

        group = Group.objects.filter(name=PSYCHOLOGIST_GROUP).first()
        categories = {}
        for i, (slug, icon, color, names) in enumerate(CATEGORIES + EXTRA_CATEGORIES):
            cat = Category.objects.filter(slug=slug).first() or Category(slug=slug)
            cat.icon, cat.color, cat.order = icon, color, i
            tr(cat, "name", names)
            cat.save()
            categories[slug] = cat

        authors = {}
        for data in PSYCHOLOGISTS + EXTRA_PSYCHOLOGISTS:
            user, created = User.objects.get_or_create(
                username=data["username"],
                defaults={k: v for k, v in data.items() if k != "username"} | {"role": User.Role.PSYCHOLOGIST, "is_verified": True, "is_staff": True},
            )
            if created:
                user.set_unusable_password()
                user.save()
            changed = not user.is_staff
            user.is_staff = True  # verified psychologists use the studio (admin)
            for field, value in PROFILE_DEFAULTS.get(user.username, {}).items():
                if not getattr(user, field):
                    setattr(user, field, value)
                    changed = True
            if changed:
                user.save()
            if group:
                user.groups.add(group)
            authors[data["username"]] = user

        created_topics = refreshed = 0
        for data in TOPICS + EXTRA_TOPICS:
            topic = Topic.objects.filter(slug=data["slug"]).first()
            if topic and not options["refresh"]:
                continue
            if topic is None:
                topic = Topic(
                    slug=data["slug"],
                    category=categories[data["category"]],
                    author=authors[data["author"]],
                    icon=data["icon"],
                    color=data["color"],
                    level=data["level"],
                    duration_minutes=data["minutes"],
                    tags=data["tags"],
                    is_published=True,
                )
                created_topics += 1
            else:
                refreshed += 1
            for field in ("title", "summary", "goal", "description"):
                tr(topic, field, data[field])
            topic.save()
            for order, s in enumerate(data["steps"], start=1):
                step = topic.steps.filter(order=order).first() or Step(topic=topic, order=order)
                step.kind = s["kind"]
                tr(step, "title", s["title"])
                tr(step, "body", s.get("body", ("", "", "", "")))
                if "breathing" in s:
                    step.inhale_seconds, step.hold_seconds, step.exhale_seconds, step.cycles = s["breathing"]
                if "results" in s:
                    for field, values in zip(("result_low", "result_mid", "result_high"), s["results"]):
                        tr(step, field, values)
                step.save()
                for q_order, (text, options_text) in enumerate(s.get("questions", []), start=1):
                    question = step.questions.filter(order=q_order).first() or QuizQuestion(step=step, order=q_order)
                    tr(question, "text", text)
                    tr(question, "options", options_text)
                    question.save()
        self.stdout.write(self.style.SUCCESS(f"Demo content ready ({created_topics} new, {refreshed} refreshed topic(s))."))
