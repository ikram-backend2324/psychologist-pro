"""Extra demo content (self-discovery test, conflict situation game). Imported by seed_demo; values are (uz, kaa, ru, en)."""

AGREE_OPTIONS = (
    "Ha, bu men haqimda | 2\nQisman | 1\nYo‘q | 0",
    "Awa, bul men haqqımda | 2\nBir az | 1\nYaq | 0",
    "Да, это про меня | 2\nОтчасти | 1\nНет | 0",
    "Yes, that's me | 2\nPartly | 1\nNo | 0",
)

EXTRA_CATEGORIES = [
    ("self-discovery", "🔎", "amber", ("O‘zini kashf etish", "Ózin tanıw", "Самопознание", "Self-discovery")),
]

EXTRA_PSYCHOLOGISTS = [
    {
        "username": "gulnora.saidova",
        "first_name": "Gulnora",
        "last_name": "Saidova",
        "specialization": "Bolalar va o‘smirlar psixologi",
        "experience_years": 7,
        "bio": "Bolalar, o‘smirlar va ota-onalar bilan ishlaydi: nizolar, maktab stressi, o‘ziga baho.",
        "age_groups": "children,teens",
        "spoken_languages": "uz,kaa,ru",
    },
]

# Profile details for the original demo psychologists (filled in only when empty).
PROFILE_DEFAULTS = {
    "dilnoza.karimova": {"age_groups": "teens,adults", "spoken_languages": "uz,ru,en"},
    "aziz.rahimov": {"age_groups": "adults,seniors", "spoken_languages": "uz,kaa,ru"},
}

EXTRA_TOPICS = [
    {
        "slug": "know-yourself",
        "category": "self-discovery",
        "author": "dilnoza.karimova",
        "icon": "🔎",
        "color": "amber",
        "level": "beginner",
        "minutes": 10,
        "tags": "self-knowledge, personality, confidence",
        "title": ("O‘zingizni taniying: introvert yoki ekstravert?", "Ózińizdi tanıń: introvert pe yamasa ekstravert pe?", "Узнай себя: интроверт или экстраверт?", "Know yourself: introvert or extrovert?"),
        "summary": (
            "Energiyangizni nimadan olishingizni bilib oling va kuchli tomonlaringizdan foydalaning.",
            "Energiyańızdı neden alatuǵınıńızdı bilip alıń hám kúshli táreplerińizden paydalanıń.",
            "Узнайте, откуда вы берёте энергию, и используйте свои сильные стороны.",
            "Find out where you get your energy from and use your strengths.",
        ),
        "goal": (
            "O‘z xarakteringizni tushunasiz va dam olish usulingizni topasiz.",
            "Óz minezińizdi túsinesiz hám dem alıw usılıńızdı tabasız.",
            "Вы поймёте свой характер и найдёте свой способ отдыхать.",
            "You will understand your temperament and find your way to recharge.",
        ),
        "description": ("", "", "", ""),
        "steps": [
            {
                "kind": "lesson",
                "title": ("Ichki energiya qayerdan keladi?", "Energiya qaydan keledi?", "Откуда берётся энергия?", "Where does your energy come from?"),
                "body": (
                    "Introvertlar yolg‘izlikda kuch to‘playdi, ekstravertlar esa odamlar orasida. Ikkalasi ham normal — yaxshi yoki yomon xarakter yo‘q.\n\nO‘zingizni bilsangiz, charchoqni oldindan sezasiz va o‘zingizga mos dam olishni tanlaysiz.",
                    "Introvertler jalǵızlıqta kúsh toplaydı, ekstravertler bolsa adamlar arasında. Ekewi de qalıptı — jaqsı yamasa jaman minez joq.\n\nÓzińizdi bilseńiz, sharshawdı aldınnan sezesiz hám ózińizge say dem alıwdı tańlaysız.",
                    "Интроверты восстанавливаются в одиночестве, экстраверты — среди людей. Оба варианта нормальны — нет хорошего или плохого характера.\n\nЗная себя, вы заранее замечаете усталость и выбираете подходящий отдых.",
                    "Introverts recharge alone, extroverts recharge with people. Both are normal — there is no good or bad temperament.\n\nKnowing yourself helps you notice tiredness early and choose the right kind of rest.",
                ),
            },
            {
                "kind": "quiz",
                "title": ("Test: Mening energiyam", "Test: Meniń energiyam", "Тест: моя энергия", "Test: my energy"),
                "body": ("Birinchi xayolingizga kelgan javobni tanlang.", "Birinshi oyıńızǵa kelgen juwaptı tańlań.", "Выбирайте первый ответ, который приходит в голову.", "Pick the first answer that comes to mind."),
                "results": (
                    (
                        "Siz ko‘proq introvertsiz. Sokin dam olish, kitob va yaqin do‘st bilan suhbat sizga kuch beradi. Bu sizning kuchingiz: chuqur o‘ylaysiz va yaxshi tinglaysiz.",
                        "Siz kóbirek introvertsiz. Tınısh dem alıw, kitap hám jaqın dos penen sáwbet sizge kúsh beredi. Bul sizdiń kúshińiz: tereń oylaysız hám jaqsı tıńlaysız.",
                        "Вы скорее интроверт. Вам дают силы тихий отдых, книги и разговор с близким другом. Это ваша сила: вы глубоко думаете и хорошо слушаете.",
                        "You lean introvert. Quiet rest, books and talks with a close friend recharge you. That's your strength: you think deeply and listen well.",
                    ),
                    (
                        "Siz ambivertsiz — vaziyatga qarab ham yolg‘izlikdan, ham odamlardan kuch olasiz. Muvozanatni saqlang.",
                        "Siz ambivertsiz — jaǵdayǵa qarap hám jalǵızlıqtan, hám adamlardan kúsh alasız. Teń salmaqlılıqtı saqlań.",
                        "Вы амбиверт — в зависимости от ситуации заряжаетесь и в одиночестве, и с людьми. Сохраняйте баланс.",
                        "You are an ambivert — you recharge both alone and with people depending on the situation. Keep the balance.",
                    ),
                    (
                        "Siz ko‘proq ekstravertsiz. Odamlar, harakat va yangi tanishuvlar sizga kuch beradi. Ba’zan tinch dam olishni ham rejalashtiring.",
                        "Siz kóbirek ekstravertsiz. Adamlar, háreket hám jańa tanısıwlar sizge kúsh beredi. Geyde tınısh dem alıwdı da rejelestiriń.",
                        "Вы скорее экстраверт. Вам дают силы люди, движение и новые знакомства. Иногда планируйте и тихий отдых.",
                        "You lean extrovert. People, movement and new friends recharge you. Plan some quiet rest now and then too.",
                    ),
                ),
                "questions": [
                    (("Katta davradan keyin o‘zimni quvvatga to‘lgan his qilaman.", "Úlken jıyınnan keyin ózimdi quwatqa tolǵan sezemen.", "После большой компании я чувствую прилив сил.", "After a big gathering I feel full of energy."), AGREE_OPTIONS),
                    (("Notanish odamlar bilan oson gaplashaman.", "Tanıs emes adamlar menen ańsat sóylesemen.", "Мне легко заговорить с незнакомыми людьми.", "I easily talk to strangers."), AGREE_OPTIONS),
                    (("O‘ylashdan ko‘ra avval gapirib yuboraman.", "Kóbinese áweli aytıp, keyin oylayman.", "Я чаще сначала говорю, потом думаю.", "I tend to speak first and think later."), AGREE_OPTIONS),
                    (("Dam olish kunini do‘stlar bilan o‘tkazishni yoqtiraman.", "Dem alıs kúnlerin doslar menen ótkeriwdi jaqsı kóremen.", "Я люблю проводить выходные с друзьями.", "I like spending weekends with friends."), AGREE_OPTIONS),
                    (("Diqqat markazida bo‘lish menga yoqadi.", "Dıqqat orayında bolıw maǵan unaydı.", "Мне нравится быть в центре внимания.", "I enjoy being the centre of attention."), AGREE_OPTIONS),
                ],
            },
            {
                "kind": "reflection",
                "title": ("Mulohaza", "Oylanıw", "Размышление", "Reflection"),
                "body": (
                    "Natija sizga mos keldimi? Qanday dam olish sizga eng ko‘p kuch beradi?",
                    "Nátiyje sizge say keldi me? Qanday dem alıw sizge eń kóp kúsh beredi?",
                    "Совпал ли результат с вашими ощущениями? Какой отдых даёт вам больше всего сил?",
                    "Does the result feel right? What kind of rest gives you the most energy?",
                ),
            },
        ],
    },
    {
        "slug": "solving-conflicts",
        "category": "relationships",
        "author": "gulnora.saidova",
        "icon": "🤝",
        "color": "rose",
        "level": "beginner",
        "minutes": 12,
        "tags": "conflict, family, communication, teens",
        "title": ("Janjalsiz nizo: muammoni birga hal qilamiz", "Urısıssız kelispewshilik: máseleni birge sheshemiz", "Конфликт без ссоры: решаем проблему вместе", "Conflict without fights: solve it together"),
        "summary": (
            "Uyda, maktabda va do‘stlar bilan nizolarni tinch hal qilishni o‘yin orqali mashq qiling.",
            "Úyde, mektepte hám doslar menen kelispewshiliklerdi tınısh sheshiwdi oyın arqalı shınıqtırıń.",
            "Тренируйтесь мирно решать конфликты дома, в школе и с друзьями — в форме игры.",
            "Practise solving conflicts at home, at school and with friends peacefully — as a game.",
        ),
        "goal": (
            "Nizoli vaziyatda to‘g‘ri qaror qabul qilish yo‘lini topasiz.",
            "Kelispewshilik jaǵdayında durıs sheshim qabıl etiw jolın tabasız.",
            "Вы найдёте, как принимать верные решения в конфликтной ситуации.",
            "You will find a way to make good decisions in a conflict.",
        ),
        "description": ("", "", "", ""),
        "steps": [
            {
                "kind": "lesson",
                "title": ("Nizo — bu urush emas", "Kelispewshilik — bul urıs emes", "Конфликт — это не война", "A conflict is not a war"),
                "body": (
                    "Nizo — ikki xil ehtiyojning to‘qnashuvi. Maqsad g‘alaba emas, ikkala tomon uchun ham yechim topish.\n\nUch qadam: 1) to‘xtang va nafas oling; 2) o‘z his-tuyg‘ungizni «men» bilan ayting; 3) birga yechim izlang.",
                    "Kelispewshilik — eki túrli mútajliktiń soqlıǵısıwı. Maqset jeńis emes, eki tárep ushın da sheshim tabıw.\n\nÚsh qádem: 1) toqtań hám dem alıń; 2) óz sezimińizdi «men» menen aytıń; 3) birge sheshim izleń.",
                    "Конфликт — это столкновение двух разных потребностей. Цель не победить, а найти решение для обеих сторон.\n\nТри шага: 1) остановитесь и вдохните; 2) скажите о своих чувствах через «я»; 3) ищите решение вместе.",
                    "A conflict is a clash of two different needs. The goal is not to win but to find a solution for both sides.\n\nThree steps: 1) pause and breathe; 2) say how you feel using “I”; 3) look for a solution together.",
                ),
            },
            {
                "kind": "scenario",
                "title": ("O‘yin: Siz nima qilardingiz?", "Oyın: Siz ne qılar edińiz?", "Игра: как бы вы поступили?", "Game: what would you do?"),
                "body": (
                    "Har bir vaziyatda o‘zingizga eng to‘g‘ri tuyulgan javobni tanlang va fikr-mulohazani o‘qing.",
                    "Hár bir jaǵdayda ózińizge eń durıs kóringen juwaptı tańlań hám pikirdi oqıń.",
                    "В каждой ситуации выберите вариант, который кажется вам верным, и прочитайте отзыв.",
                    "In each situation pick the option that feels right, then read the feedback.",
                ),
                "questions": [
                    (
                        (
                            "Ukangiz so‘ramasdan telefoningizni olib, o‘yin o‘ynab o‘tiribdi.",
                            "Inińiz soramastan telefonıńızdı alıp, oyın oynap otır.",
                            "Младший брат без спроса взял ваш телефон и играет.",
                            "Your younger brother took your phone without asking and is playing a game.",
                        ),
                        (
                            "Telefonni tortib olib, baqiraman | 0 | Baqiriq nizoni kuchaytiradi va uka xafa bo‘ladi.\nXotirjam aytaman: «So‘ramay olganing menga yoqmadi. Keyingi safar so‘ra» | 2 | Ajoyib! «Men» bilan gapirish his-tuyg‘uni hujumsiz yetkazadi.\nIndamay, keyin ota-onamga shikoyat qilaman | 1 | Kattalardan yordam so‘rash mumkin, lekin avval o‘zingiz gaplashib ko‘ring.",
                            "Telefondı tartıp alıp, baqıraman | 0 | Baqırıq kelispewshilikti kúsheytedi hám inińiz renjiydi.\nTınısh aytaman: «Soramay alǵanıń maǵan unamadı. Keyingi ret sora» | 2 | Ájayıp! «Men» menen sóylew sezimdi hújimsiz jetkeredi.\nÚndemey, keyin ata-anama aytaman | 1 | Úlkenlerden járdem soraw múmkin, biraq áweli ózińiz sóylesip kóriń.",
                            "Вырву телефон и накричу | 0 | Крик усиливает конфликт, и брат обидится.\nСпокойно скажу: «Мне неприятно, что ты взял без спроса. В следующий раз спроси» | 2 | Отлично! Фраза через «я» передаёт чувства без нападения.\nПромолчу, а потом пожалуюсь родителям | 1 | Можно попросить помощи у взрослых, но сначала попробуйте поговорить сами.",
                            "Grab the phone back and shout | 0 | Shouting makes the conflict bigger and your brother gets hurt.\nCalmly say: “I didn't like that you took it without asking. Ask next time” | 2 | Great! An “I” message shares your feelings without attacking.\nSay nothing and complain to my parents later | 1 | Asking adults for help is okay, but try talking first.",
                        ),
                    ),
                    (
                        (
                            "Sinfdoshingiz guruh loyihasida o‘z qismini qilmadi, ertaga topshirish kerak.",
                            "Klaslasıńız topar joybarında óz bólegin islemedi, erteń tapsırıw kerek.",
                            "Одноклассник не сделал свою часть группового проекта, а сдавать завтра.",
                            "A classmate didn't do their part of the group project, and it's due tomorrow.",
                        ),
                        (
                            "Hammaning oldida uni uyaltiraman | 0 | Uyaltirish munosabatni buzadi va ishni tezlashtirmaydi.\nU bilan yakkama-yakka gaplashib, sababini so‘rayman va yordam taklif qilaman | 2 | Zo‘r! Sababini bilish va birga reja tuzish — eng samarali yo‘l.\nHammasini o‘zim qilib qo‘yaman | 1 | Loyiha tugaydi, lekin muammo keyingi safar yana takrorlanadi.",
                            "Hámmeniń aldında onı uyaltaman | 0 | Uyaltıw qatnastı buzadı hám isti tezletpeydi.\nOnıń menen jeke sóylesip, sebebin sorayman hám járdem usınaman | 2 | Ájayıp! Sebebin biliw hám birge joba dúziw — eń nátiyjeli jol.\nHámmesin ózim islep qoyaman | 1 | Joybar pitedi, biraq másele keyingi ret jáne qaytalanadı.",
                            "Пристыжу его при всех | 0 | Стыд разрушает отношения и не ускоряет работу.\nПоговорю с ним наедине, спрошу причину и предложу помощь | 2 | Отлично! Узнать причину и составить план вместе — самый действенный путь.\nСделаю всё сам | 1 | Проект будет готов, но проблема повторится в следующий раз.",
                            "Shame them in front of everyone | 0 | Shaming damages the relationship and doesn't speed up the work.\nTalk to them privately, ask why, and offer help | 2 | Great! Finding the reason and making a plan together works best.\nDo everything myself | 1 | The project gets done, but the problem will repeat next time.",
                        ),
                    ),
                    (
                        (
                            "Ota-onangiz kechqurun do‘stlaringiz bilan chiqishingizga ruxsat bermadi.",
                            "Ata-anańız keshte doslarıńız benen shıǵıwıńızǵa ruxsat bermedi.",
                            "Родители не разрешили вам вечером пойти гулять с друзьями.",
                            "Your parents didn't let you go out with friends in the evening.",
                        ),
                        (
                            "Eshikni qarsillatib yopib, xonamga kirib ketaman | 0 | Hissiyot tushunarli, lekin bu suhbat imkoniyatini yopadi.\nNega xavotir olishlarini so‘rayman va kelishuv taklif qilaman: soat 21:00 gacha qaytaman | 2 | Juda yaxshi! Ularning xavotirini tushunish va kelishuv taklif qilish ishonchni oshiradi.\nYashirincha baribir chiqib ketaman | 0 | Bu ishonchni buzadi va xavfli bo‘lishi mumkin.",
                            "Esikti qattı jawıp, bólmeme kirip ketemen | 0 | Sezim túsinikli, biraq bul sáwbet imkaniyatın jabadı.\nNe ushın qáweterlenetuǵının sorayman hám kelisim usınaman: saat 21:00-ge shekem qaytaman | 2 | Júdá jaqsı! Olardıń qáweterin túsiniw hám kelisim usınıw isenimdi asıradı.\nJasırın túrde bári bir shıǵıp ketemen | 0 | Bul isenimdi buzadı hám qáwipli bolıwı múmkin.",
                            "Хлопну дверью и уйду в комнату | 0 | Чувства понятны, но так закрывается возможность договориться.\nСпрошу, почему они волнуются, и предложу договор: вернусь до 21:00 | 2 | Очень хорошо! Понимание их тревоги и компромисс укрепляют доверие.\nВсё равно тайком уйду | 0 | Это разрушает доверие и может быть опасно.",
                            "Slam the door and go to my room | 0 | The feeling is understandable, but it closes the door to talking.\nAsk why they worry and offer a deal: I'll be back by 9 pm | 2 | Very good! Understanding their worry and offering a compromise builds trust.\nSneak out anyway | 0 | This breaks trust and can be dangerous.",
                        ),
                    ),
                ],
            },
            {
                "kind": "reflection",
                "title": ("Mulohaza", "Oylanıw", "Размышление", "Reflection"),
                "body": (
                    "Yaqinda bo‘lgan bir nizoni eslang. Endi uni qanday hal qilgan bo‘lardingiz?",
                    "Jaqında bolǵan bir kelispewshilikti eslań. Endi onı qalay sheshken bolar edińiz?",
                    "Вспомните недавний конфликт. Как бы вы решили его теперь?",
                    "Think of a recent conflict. How would you solve it now?",
                ),
            },
        ],
    },
]
