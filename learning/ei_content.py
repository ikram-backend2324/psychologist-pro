"""Emotional intelligence course: 8 topics built on the scientific guide
"Hissiy intellekt" (diss ilimiy qo‘llanma). Each topic follows the same structure:
scientific basis (lesson) -> self-test -> practical exercise -> self-help reflection.
All texts are (uz, kaa, ru, en). Seeded by `python manage.py seed_ei`.
"""

FREQ = (
    "Hech qachon | 0\nBa’zan | 1\nKo‘pincha | 2\nDoim | 3",
    "Hesh qashan | 0\nGeyde | 1\nKóbinese | 2\nÁrqashan | 3",
    "Никогда | 0\nИногда | 1\nЧасто | 2\nВсегда | 3",
    "Never | 0\nSometimes | 1\nOften | 2\nAlways | 3",
)
FREQ_R = (
    "Hech qachon | 3\nBa’zan | 2\nKo‘pincha | 1\nDoim | 0",
    "Hesh qashan | 3\nGeyde | 2\nKóbinese | 1\nÁrqashan | 0",
    "Никогда | 3\nИногда | 2\nЧасто | 1\nВсегда | 0",
    "Never | 3\nSometimes | 2\nOften | 1\nAlways | 0",
)

TEST_INTRO = (
    "Har bir fikrni o‘qing va o‘zingizga eng mos javobni tanlang. To‘g‘ri yoki noto‘g‘ri javob yo‘q — bu o‘zingizni kuzatish uchun.",
    "Hár bir pikirdi oqıń hám ózińizge eń say juwaptı tańlań. Durıs yamasa nadurıs juwap joq — bul ózińizdi baqlaw ushın.",
    "Прочитайте каждое утверждение и выберите самый подходящий ответ. Правильных и неправильных ответов нет — это для самонаблюдения.",
    "Read each statement and choose the answer that fits you best. There are no right or wrong answers — this is for self-observation.",
)

SCENARIO_INTRO = (
    "Har bir vaziyatni o‘qing va o‘zingiz qanday yo‘l tutishingizni tanlang. Har bir tanlovdan keyin izoh chiqadi.",
    "Hár bir jaǵdaydı oqıń hám ózińiz qalay háreket etetuǵınıńızdı tańlań. Hár bir tańlawdan keyin túsindirme shıǵadı.",
    "Прочитайте каждую ситуацию и выберите, как бы вы поступили. После каждого выбора появится пояснение.",
    "Read each situation and choose what you would do. An explanation appears after each choice.",
)


def description(uz, kaa, ru, en):
    """Topic description that names the three-part structure of every course topic."""
    return (
        uz + "\n\nMavzu tuzilishi: 🔬 ilmiy asos (dars) → 📝 o‘zini baholash testi → 🧩 amaliy mashq → ✍️ o‘zingizga yordam.",
        kaa + "\n\nTema dúzilisi: 🔬 ilimiy tiykar (sabaq) → 📝 ózin bahalaw testi → 🧩 ámeliy shınıǵıw → ✍️ ózińizge járdem.",
        ru + "\n\nСтруктура темы: 🔬 научная основа (урок) → 📝 тест самооценки → 🧩 практическое упражнение → ✍️ помоги себе сам.",
        en + "\n\nTopic structure: 🔬 scientific basis (lesson) → 📝 self-assessment test → 🧩 practical exercise → ✍️ self-help.",
    )


EI_CATEGORY = ("emotional-intelligence", "💡", "sunset", ("Hissiy intellekt", "Emocional intellekt", "Эмоциональный интеллект", "Emotional intelligence"))

EI_AUTHOR = {
    "username": "farida",
    "first_name": "Farida",
    "last_name": "",
    "specialization": "Psixolog",
    "experience_years": 0,
    "bio": "Hissiy intellekt kursi muallifi: ilmiy manbalarga asoslangan darslar va talabalar uchun amaliy mashqlar.",
    "age_groups": "teens,adults",
    "spoken_languages": "uz,kaa,ru",
}

TOPICS_1 = [
    # ------------------------------------------------------------------ 1
    {
        "slug": "ei-1-what-is-emotional-intelligence",
        "order": 1,
        "icon": "💡",
        "color": "sunset",
        "level": "beginner",
        "minutes": 15,
        "tags": "emotional intelligence, emotions, self-knowledge",
        "sources": (
            "Salovey P., Mayer J. D. Emotional intelligence // Imagination, Cognition and Personality. – 1990. – Vol. 9(3). – P. 185–211.\n"
            "Mayer J. D., Salovey P., Caruso D. R. MSCEIT User’s Manual. – Toronto: MHS, 2002.\n"
            "Goleman D. Emotional Intelligence: Why It Can Matter More Than IQ. – New York: Bantam Books, 1995.\n"
            "Gardner H. Frames of Mind: The Theory of Multiple Intelligences. – New York: Basic Books, 1983."
        ),
        "title": (
            "Hissiy intellekt nima?",
            "Emocional intellekt degen ne?",
            "Что такое эмоциональный интеллект?",
            "What is emotional intelligence?",
        ),
        "summary": (
            "Mayer va Salovey modeli: his-tuyg‘ularni idrok etish, ulardan foydalanish, tushunish va boshqarish.",
            "Mayer hám Salovey modeli: sezimlerdi qabıllaw, olardan paydalanıw, túsiniw hám basqarıw.",
            "Модель Майера и Сэловея: восприятие, использование, понимание и управление эмоциями.",
            "The Mayer–Salovey model: perceiving, using, understanding and managing emotions.",
        ),
        "goal": (
            "Hissiy intellektning to‘rt qobiliyatini bilasiz va o‘zingizda qaysi biri kuchli ekanini aniqlaysiz.",
            "Emocional intellekttiń tórt qábiletin bilesiz hám ózińizde qaysısı kúshli ekenin anıqlaysız.",
            "Вы узнаете четыре способности эмоционального интеллекта и поймёте, какая из них у вас сильнее.",
            "You will know the four abilities of emotional intelligence and find out which one is strongest in you.",
        ),
        "description": description(
            "Kursning birinchi mavzusi: hissiy intellekt qanday paydo bo‘lgan tushuncha, u IQ dan nimasi bilan farq qiladi va qanday qobiliyatlardan tashkil topadi.",
            "Kurstıń birinshi teması: emocional intellekt qalay payda bolǵan túsinik, ol IQ dan nesi menen parıq qıladı hám qanday qábiletlerden ibarat.",
            "Первая тема курса: откуда появилось понятие эмоционального интеллекта, чем он отличается от IQ и из каких способностей состоит.",
            "The first topic of the course: where the idea of emotional intelligence came from, how it differs from IQ and which abilities it consists of.",
        ),
        "steps": [
            {
                "kind": "lesson",
                "title": ("Ilmiy asos: his-tuyg‘u va aql do‘st", "Ilimiy tiykar: sezim hám aqıl dos", "Научная основа: эмоции и разум — союзники", "Scientific basis: emotions and reason are allies"),
                "body": (
                    "Uzoq vaqt his-tuyg‘ular aqlga xalaqit beradi, deb hisoblangan. Zamonaviy psixologiya buni rad etdi: his-tuyg‘ular inson va atrof-muhit o‘rtasidagi munosabat haqida axborot beruvchi signallardir. Masalan, quvonch yaxshi voqeani, qayg‘u esa yo‘qotishni bildiradi.\n\n"
                    "«Hissiy intellekt» atamasini 1990-yilda John Mayer va Peter Salovey ilmiy muomalaga kiritgan. Bu — his-tuyg‘ularni aniqlash, tushunish va ular asosida fikrlash hamda muammolarni hal qilish qobiliyati. Tushunchani Daniel Goleman (1995) ommalashtirgan.\n\n"
                    "Mayer va Salovey modelida to‘rt daraja bor: 1) his-tuyg‘ularni idrok etish (yuz, ovoz, imo-ishoradan o‘qish); 2) ulardan fikrlashda foydalanish; 3) ularni tushunish (g‘azab — adolatsizlikdan, qo‘rquv — xavfdan); 4) ularni boshqarish — eng yuqori daraja.\n\n"
                    "Muhim xulosa: IQ asosan o‘zgarmaydi, hissiy intellekt esa yosh va tajriba bilan o‘sadi. Uni mashq orqali rivojlantirish mumkin — bu kurs aynan shunga bag‘ishlangan.",
                    "Uzaq waqıt sezimler aqılǵa kesent beredi dep esaplanǵan. Házirgi psixologiya bunı biykarladı: sezimler adam hám átirap ortasındaǵı qatnas haqqında maǵlıwmat beretuǵın signallar. Mısalı, quwanısh jaqsı waqıyanı, qayǵı bolsa joǵaltıwdı bildiredi.\n\n"
                    "«Emocional intellekt» terminin 1990-jılı John Mayer hám Peter Salovey ilimge kirgizgen. Bul — sezimlerdi anıqlaw, túsiniw hám solar tiykarında oylaw hám máselelerdi sheshiw qábileti. Túsinikti Daniel Goleman (1995) keń tarqattı.\n\n"
                    "Mayer hám Salovey modelinde tórt dáreje bar: 1) sezimlerdi qabıllaw (júz, dawıs, ım-isharadan oqıw); 2) olardan oylawda paydalanıw; 3) olardı túsiniw (ashıw — ádilsizlikten, qorqıw — qáwipten); 4) olardı basqarıw — eń joqarı dáreje.\n\n"
                    "Áhmiyetli juwmaq: IQ tiykarınan ózgermeydi, al emocional intellekt jas hám tájiriybe menen ósedi. Onı shınıǵıw arqalı rawajlandırıwǵa boladı — bul kurs usıǵan arnalǵan.",
                    "Долгое время считалось, что эмоции мешают разуму. Современная психология это опровергла: эмоции — сигналы, которые несут информацию об отношениях человека с окружающим миром. Например, радость говорит о хорошем событии, грусть — о потере.\n\n"
                    "Термин «эмоциональный интеллект» ввели в 1990 году Джон Майер и Питер Сэловей. Это способность распознавать и понимать эмоции и опираться на них в мышлении и решении задач. Популярным понятие сделал Дэниел Гоулман (1995).\n\n"
                    "В модели Майера и Сэловея четыре уровня: 1) восприятие эмоций (по лицу, голосу, жестам); 2) использование их в мышлении; 3) понимание эмоций (гнев — от несправедливости, страх — от опасности); 4) управление ими — высший уровень.\n\n"
                    "Важный вывод: IQ почти не меняется, а эмоциональный интеллект растёт с возрастом и опытом. Его можно развивать упражнениями — этому и посвящён курс.",
                    "For a long time emotions were thought to get in the way of reason. Modern psychology disproved this: emotions are signals that carry information about our relationship with the world. Joy points to a good event, sadness to a loss.\n\n"
                    "The term “emotional intelligence” was introduced in 1990 by John Mayer and Peter Salovey. It is the ability to recognise and understand emotions and use them in thinking and problem solving. Daniel Goleman (1995) made the idea popular.\n\n"
                    "The Mayer–Salovey model has four levels: 1) perceiving emotions (in faces, voices, gestures); 2) using them in thinking; 3) understanding them (anger comes from injustice, fear from danger); 4) managing them — the highest level.\n\n"
                    "The key point: IQ hardly changes, but emotional intelligence grows with age and experience. It can be trained with practice — which is what this course is for.",
                ),
            },
            {
                "kind": "quiz",
                "title": ("Test: Mening hissiy intellekt profilim", "Test: Meniń emocional intellekt profilim", "Тест: мой профиль эмоционального интеллекта", "Test: my emotional intelligence profile"),
                "body": TEST_INTRO,
                "results": (
                    (
                        "Hozircha his-tuyg‘ularingizni sezish va nomlash qiyin. Bu ko‘nikma — xuddi mushak kabi. Har kuni kechqurun bugun nimani his qilganingizni bitta so‘z bilan yozib boring.",
                        "Házirshe sezimlerińizdi sezip, atın ataw qıyın. Bul kónlikpe — bulshıq et sıyaqlı. Hár kúni keshte búgin neni sezgenińizdi bir sóz benen jazıp barıń.",
                        "Пока вам непросто замечать и называть свои чувства. Это навык, как мышца. Каждый вечер записывайте одним словом, что вы сегодня чувствовали.",
                        "Noticing and naming your feelings is still hard for you. It is a skill, like a muscle. Every evening write down in one word what you felt today.",
                    ),
                    (
                        "Sizda yaxshi asos bor: ko‘pincha his-tuyg‘ularingizni sezasiz. Keyingi qadam — ularning sababini tushunish va qiyin paytlarda ham xotirjam qolish.",
                        "Sizde jaqsı tiykar bar: kóbinese sezimlerińizdi sezesiz. Keyingi qádem — olardıń sebebin túsiniw hám qıyın waqıtta da tınısh qalıw.",
                        "У вас хорошая база: вы часто замечаете свои чувства. Следующий шаг — понимать их причины и сохранять спокойствие в трудные моменты.",
                        "You have a good base: you often notice your feelings. The next step is to understand their causes and stay calm in difficult moments.",
                    ),
                    (
                        "Ajoyib! Siz his-tuyg‘ularni yaxshi sezasiz va boshqarasiz. Kursning keyingi mavzularida bu qobiliyatni boshqalar bilan munosabatlarda qo‘llashni o‘rganasiz.",
                        "Ájayıp! Siz sezimlerdi jaqsı sezesiz hám basqarasız. Kurstıń keyingi temalarında bul qábiletti basqalar menen qatnasta qollanıwdı úyrenesiz.",
                        "Отлично! Вы хорошо замечаете эмоции и управляете ими. В следующих темах курса вы научитесь применять это в отношениях с людьми.",
                        "Excellent! You notice and manage emotions well. In the next topics you will learn to use this in your relationships.",
                    ),
                ),
                "questions": [
                    (("Hozir qanday his-tuyg‘u boshdan kechirayotganimni aniq ayta olaman.", "Házir qanday sezimdi bastan keshirip atırǵanımdı anıq ayta alaman.", "Я могу точно сказать, какое чувство испытываю сейчас.", "I can say exactly what I am feeling right now."), FREQ),
                    (("Odamning yuzi va ovozidan uning kayfiyatini sezaman.", "Adamnıń júzi hám dawısınan onıń kewil-kúyin sezemen.", "По лицу и голосу человека я чувствую его настроение.", "I can tell someone’s mood from their face and voice."), FREQ),
                    (("Muhim qaror qabul qilishda his-tuyg‘ularimni ham hisobga olaman.", "Áhmiyetli qarar qabıllaǵanda sezimlerimdi de esapqa alaman.", "Принимая важное решение, я учитываю и свои чувства.", "When making an important decision I take my feelings into account too."), FREQ),
                    (("Nega xafa yoki jahlim chiqqanini tushunolmay qolaman.", "Ne ushın renjigenimdi yamasa ashıwlanǵanımdı túsine almay qalaman.", "Я не могу понять, почему расстроился или разозлился.", "I can’t understand why I got upset or angry."), FREQ_R),
                    (("Kuchli his-tuyg‘u paytida ham o‘zimni bosib ola olaman.", "Kúshli sezim waqtında da ózimdi tuta alaman.", "Даже при сильных эмоциях я могу держать себя в руках.", "Even during strong emotions I can keep myself together."), FREQ),
                ],
            },
            {
                "kind": "cards",
                "title": ("Amaliy mashq: To‘rt qobiliyat", "Ámeliy shınıǵıw: Tórt qábilet", "Практика: четыре способности", "Practice: the four abilities"),
                "body": (
                    "Do‘stingizning yuzidan xafaligini sezdim | 1-qobiliyat: his-tuyg‘ularni idrok etish\nImtihondan oldingi hayajon meni yaxshiroq tayyorlanishga undadi | 2-qobiliyat: his-tuyg‘udan fikrlashda foydalanish\nG‘azabim adolatsizlikdan kelib chiqqanini angladim | 3-qobiliyat: his-tuyg‘ularni tushunish\nJahlim chiqsa ham ovozimni ko‘tarmadim, avval nafas oldim | 4-qobiliyat: his-tuyg‘ularni boshqarish\nIQ va hissiy intellektning farqi? | IQ deyarli o‘zgarmaydi, hissiy intellekt mashq bilan o‘sadi",
                    "Dostımnıń júzinen renjigenin sezdim | 1-qábilet: sezimlerdi qabıllaw\nImtixan aldındaǵı tolǵanıw meni jaqsıraq tayarlanıwǵa iyterdi | 2-qábilet: sezimnen oylawda paydalanıw\nAshıwım ádilsizlikten kelip shıqqanın túsindim | 3-qábilet: sezimlerdi túsiniw\nAshıwım kelse de dawısımdı kótermedim, aldın dem aldım | 4-qábilet: sezimlerdi basqarıw\nIQ hám emocional intellekttiń parqı? | IQ derlik ózgermeydi, emocional intellekt shınıǵıw menen ósedi",
                    "По лицу друга я заметил, что он расстроен | Способность 1: восприятие эмоций\nВолнение перед экзаменом заставило меня лучше подготовиться | Способность 2: использование эмоций в мышлении\nЯ понял, что мой гнев вызван несправедливостью | Способность 3: понимание эмоций\nХоть я и разозлился, но не повысил голос — сначала сделал вдох | Способность 4: управление эмоциями\nЧем IQ отличается от эмоционального интеллекта? | IQ почти не меняется, а эмоциональный интеллект растёт с практикой",
                    "I noticed from my friend’s face that he was upset | Ability 1: perceiving emotions\nNerves before the exam made me prepare better | Ability 2: using emotions in thinking\nI realised my anger came from injustice | Ability 3: understanding emotions\nI was angry but didn’t raise my voice — I took a breath first | Ability 4: managing emotions\nHow does IQ differ from emotional intelligence? | IQ hardly changes; emotional intelligence grows with practice",
                ),
            },
            {
                "kind": "reflection",
                "title": ("O‘zingizga yordam: kuchli tomoningiz", "Ózińizge járdem: kúshli tárepińiz", "Помоги себе: ваша сильная сторона", "Self-help: your strength"),
                "body": (
                    "To‘rt qobiliyatdan qaysi biri sizda eng kuchli, qaysi biri esa eng zaif? Zaif qobiliyatni rivojlantirish uchun shu hafta qilishingiz mumkin bo‘lgan bitta kichik ishni yozing.",
                    "Tórt qábiletten qaysısı sizde eń kúshli, qaysısı eń álsiz? Álsiz qábiletti rawajlandırıw ushın usı hápte isley alatuǵın bir kishi isti jazıń.",
                    "Какая из четырёх способностей у вас самая сильная, а какая самая слабая? Напишите одно небольшое дело, которое вы можете сделать на этой неделе, чтобы развить слабую.",
                    "Which of the four abilities is your strongest and which is your weakest? Write one small thing you can do this week to develop the weaker one.",
                ),
            },
        ],
    },
    # ------------------------------------------------------------------ 2
    {
        "slug": "ei-2-nature-of-emotions",
        "order": 2,
        "icon": "🧬",
        "color": "violet",
        "level": "beginner",
        "minutes": 15,
        "tags": "emotions, brain, stress, self-knowledge",
        "sources": (
            "Darwin C. The Expression of the Emotions in Man and Animals. – London: John Murray, 1872.\n"
            "LeDoux J. The Emotional Brain: The Mysterious Underpinnings of Emotional Life. – New York: Simon & Schuster, 1996.\n"
            "Damasio A. R. Descartes’ Error: Emotion, Reason, and the Human Brain. – New York: Putnam, 1994.\n"
            "Gross J. J. The emerging field of emotion regulation: An integrative review // Review of General Psychology. – 1998. – Vol. 2(3). – P. 271–299.\n"
            "Lemberg B. Emotsional intellekt: aql va his-tuyg‘ular o‘rtasidagi muloqot. – 2013."
        ),
        "title": (
            "His-tuyg‘ular nima uchun kerak?",
            "Sezimler ne ushın kerek?",
            "Зачем нам эмоции?",
            "Why do we need emotions?",
        ),
        "summary": (
            "His-tuyg‘ularning biologik vazifasi, miya mexanizmlari va ularni bostirish nima uchun zararli.",
            "Sezimlerdiń biologiyalıq wazıypası, miy mexanizmleri hám olardı basıw ne ushın ziyanlı.",
            "Биологическая роль эмоций, механизмы мозга и почему подавлять чувства вредно.",
            "The biological role of emotions, the brain behind them and why suppressing feelings hurts.",
        ),
        "goal": (
            "Har bir his-tuyg‘u — hatto g‘azab va qo‘rquv ham — foydali signal ekanini tushunasiz va ularni bostirmasdan qabul qilishni o‘rganasiz.",
            "Hár bir sezim — hátte ashıw hám qorqıw da — paydalı signal ekenin túsinesiz hám olardı baspay qabıllawdı úyrenesiz.",
            "Вы поймёте, что каждая эмоция — даже гнев и страх — полезный сигнал, и научитесь принимать чувства, не подавляя их.",
            "You will understand that every emotion — even anger and fear — is a useful signal, and learn to accept feelings without suppressing them.",
        ),
        "description": description(
            "His-tuyg‘ular tasodifiy emas: ular har doim biror sababga javob. Bu mavzuda Darwin, LeDoux va Damasio tadqiqotlari asosida his-tuyg‘ularning vazifasini ko‘rib chiqamiz.",
            "Sezimler tosınnan emes: olar hámme waqıt bir sebepke juwap. Bul temada Darwin, LeDoux hám Damasio izertlewleri tiykarında sezimlerdiń wazıypasın kórip shıǵamız.",
            "Эмоции не случайны: они всегда ответ на какую-то причину. В этой теме мы разберём роль эмоций по исследованиям Дарвина, Леду и Дамасио.",
            "Emotions are never random: they always answer some cause. In this topic we look at their role through the research of Darwin, LeDoux and Damasio.",
        ),
        "steps": [
            {
                "kind": "lesson",
                "title": ("Ilmiy asos: his-tuyg‘u — signal", "Ilimiy tiykar: sezim — signal", "Научная основа: эмоция — это сигнал", "Scientific basis: an emotion is a signal"),
                "body": (
                    "Charles Darwin (1872) ta’kidlaganidek, har qanday his-tuyg‘u — organizmning vaziyatga moslashuvchan javobi. His-tuyg‘ular baholovchi mexanizm: ular tanani tez harakatga tayyorlaydi va ehtiyojlarni qondirishga undaydi. Salbiy his-tuyg‘u ehtiyoj qondirilmaganini, ijobiy his-tuyg‘u esa qondirilganini bildiradi.\n\n"
                    "Miyada bu jarayonni limbik tizim, ayniqsa amigdala boshqaradi: u vaziyat xavfli yoki xavfsiz ekanini bir zumda baholaydi. Orbitofrontal po‘stloq esa his-tuyg‘ularni ongli fikrlash bilan bog‘laydi. A. Damasio tadqiqotlari ko‘rsatdiki, bu soha shikastlangan odamlar his-tuyg‘u bilan birga to‘g‘ri tanlov qilish qobiliyatini ham yo‘qotadi.\n\n"
                    "Har bir his-tuyg‘uning foydasi bor: g‘azab energiya beradi va o‘zini himoya qilishga undaydi; qayg‘u tiklanish va mulohaza uchun vaqt beradi; qo‘rquv xavfni oldindan sezdiradi.\n\n"
                    "Shuning uchun his-tuyg‘ularni bostirish emas, yo‘naltirish kerak. J. Gross (1998) ko‘rsatdiki, bostirish o‘zini anglashni pasaytiradi, charchoq va munosabatlarda muammolar keltirib chiqaradi. B. Lemberg aytganidek: bostirilmagan his-tuyg‘u o‘z-o‘zidan paydo bo‘ladi va o‘tib ketadi.",
                    "Charles Darwin (1872) atap ótkenindey, hár qanday sezim — organizmniń jaǵdayǵa beyimlesiwshi juwabı. Sezimler bahalawshı mexanizm: olar deneni tez háreketke tayarlaydı hám mútájliklerdi qanaatlandırıwǵa iyteredi. Unamsız sezim mútájlik qanaatlandırılmaǵanın, unamlı sezim bolsa qanaatlandırılǵanın bildiredi.\n\n"
                    "Miyda bul processti limbik sistema, ásirese amigdala basqaradı: ol jaǵday qáwipli me yamasa qáwipsiz be ekenin bir zamatta bahalaydı. Orbitofrontal qabıq bolsa sezimlerdi sanalı oylaw menen baylanıstıradı. A. Damasio izertlewleri kórsetkenindey, bul bólimi zaqımlanǵan adamlar sezim menen birge durıs tańlaw qábiletin de joǵaltadı.\n\n"
                    "Hár bir sezimniń paydası bar: ashıw energiya beredi hám ózin qorǵawǵa iyteredi; qayǵı tikleniw hám oylanıw ushın waqıt beredi; qorqıw qáwipti aldınnan sezdiredi.\n\n"
                    "Sonlıqtan sezimlerdi basıw emes, baǵdarlaw kerek. J. Gross (1998) kórsetkenindey, basıw ózin ańlawdı tómenletedi, sharshaw hám qatnaslarda máseleler payda etedi. B. Lemberg aytqanınday: basılmaǵan sezim óz-ózinen payda boladı hám ótip ketedi.",
                    "Как писал Чарльз Дарвин (1872), любая эмоция — приспособительный ответ организма на ситуацию. Эмоции работают как механизм оценки: быстро готовят тело к действию и побуждают удовлетворять потребности. Негативная эмоция сообщает, что потребность не удовлетворена, позитивная — что удовлетворена.\n\n"
                    "В мозге этим управляет лимбическая система, особенно миндалевидное тело (амигдала): оно мгновенно оценивает, опасна ситуация или нет. Орбитофронтальная кора связывает эмоции с осознанным мышлением. Исследования А. Дамасио показали: люди с повреждением этой зоны вместе с эмоциями теряют и способность делать верный выбор.\n\n"
                    "У каждой эмоции есть польза: гнев даёт энергию и побуждает защищаться; грусть даёт время на восстановление и размышление; страх заранее предупреждает об опасности.\n\n"
                    "Поэтому эмоции нужно не подавлять, а направлять. Дж. Гросс (1998) показал, что подавление снижает самопонимание, вызывает усталость и проблемы в отношениях. Как пишет Б. Лемберг, неподавленная эмоция сама возникает и сама проходит.",
                    "As Charles Darwin (1872) noted, every emotion is the body’s adaptive response to a situation. Emotions work as an appraisal system: they quickly prepare the body to act and push us to meet our needs. A negative emotion says a need is unmet; a positive one says it is met.\n\n"
                    "In the brain this is run by the limbic system, especially the amygdala, which instantly judges whether a situation is dangerous. The orbitofrontal cortex links emotions to conscious thinking. Antonio Damasio found that people with damage to this area lose not only emotions but also the ability to make good choices.\n\n"
                    "Every emotion is useful: anger gives energy and pushes us to protect ourselves; sadness gives time to recover and reflect; fear warns us of danger in advance.\n\n"
                    "So emotions should be guided, not suppressed. James Gross (1998) showed that suppression lowers self-understanding and causes exhaustion and relationship problems. As B. Lemberg puts it, an emotion that is not suppressed rises naturally and passes on its own.",
                ),
            },
            {
                "kind": "quiz",
                "title": ("Test: His-tuyg‘ularimga munosabatim", "Test: Sezimlerime qatnasım", "Тест: как я отношусь к своим чувствам", "Test: how I treat my feelings"),
                "body": TEST_INTRO,
                "results": (
                    (
                        "Siz his-tuyg‘ularni ko‘pincha bostirasiz yoki «yomon» deb hisoblaysiz. Esda tuting: his-tuyg‘u — xabar. Bugun kuchli his-tuyg‘u kelsa, unga «Sen menga nima demoqchisan?» deb savol bering.",
                        "Siz sezimlerdi kóbinese basasız yamasa «jaman» dep esaplaysız. Este tutıń: sezim — xabar. Búgin kúshli sezim kelse, oǵan «Sen maǵan ne demekshisen?» dep soraw beriń.",
                        "Вы часто подавляете чувства или считаете их «плохими». Помните: эмоция — это сообщение. Когда сегодня придёт сильное чувство, спросите его: «Что ты хочешь мне сказать?»",
                        "You often suppress feelings or consider them “bad”. Remember: an emotion is a message. When a strong feeling comes today, ask it: “What are you trying to tell me?”",
                    ),
                    (
                        "Siz his-tuyg‘ularni qisman qabul qilasiz. Ayniqsa noqulay his-tuyg‘ularni (g‘azab, qayg‘u) ham baholamasdan kuzatishni mashq qiling — ular o‘z-o‘zidan o‘tib ketadi.",
                        "Siz sezimlerdi bir qansha qabıllaysız. Ásirese jaǵımsız sezimlerdi (ashıw, qayǵı) da bahalamay baqlawdı shınıqtırıń — olar óz-ózinen ótip ketedi.",
                        "Вы отчасти принимаете свои чувства. Тренируйтесь наблюдать без оценки и неудобные эмоции (гнев, грусть) — они проходят сами.",
                        "You partly accept your feelings. Practise observing uncomfortable ones (anger, sadness) without judging — they pass on their own.",
                    ),
                    (
                        "Ajoyib! Siz his-tuyg‘ularni foydali signal sifatida qabul qilasiz. Bu sog‘lom hissiy hayotning asosi.",
                        "Ájayıp! Siz sezimlerdi paydalı signal retinde qabıllaysız. Bul salamat sezimlik ómirdiń tiykarı.",
                        "Отлично! Вы принимаете эмоции как полезные сигналы. Это основа здоровой эмоциональной жизни.",
                        "Excellent! You accept emotions as useful signals. This is the foundation of a healthy emotional life.",
                    ),
                ),
                "questions": [
                    (("Kuchli his-tuyg‘u kelsa, uni ichimga yutib, hech kimga ko‘rsatmayman.", "Kúshli sezim kelse, onı ishime jutıp, hesh kimge kórsetpeymen.", "Когда приходит сильное чувство, я прячу его и никому не показываю.", "When a strong feeling comes, I swallow it and show it to no one."), FREQ_R),
                    (("G‘azab yoki qayg‘u ham menga nimadir haqida xabar berishini tushunaman.", "Ashıw yamasa qayǵı da maǵan bir nárse haqqında xabar beretuǵının túsinemen.", "Я понимаю, что и гнев, и грусть что-то мне сообщают.", "I understand that even anger or sadness tells me something."), FREQ),
                    (("Xavotir paytida tanamdagi o‘zgarishlarni (yurak urishi, nafas) sezaman.", "Tınıshsızlıq waqtında denemdegi ózgerislerdi (júrek urıwı, dem) sezemen.", "В тревоге я замечаю изменения в теле (сердцебиение, дыхание).", "When anxious I notice changes in my body (heartbeat, breathing)."), FREQ),
                    (("«Yig‘lash — zaiflik» yoki «jahl qilish — yomon» deb o‘ylayman.", "«Jılaw — álsizlik» yamasa «ashıwlanıw — jaman» dep oylayman.", "Я думаю, что «плакать — слабость» или «злиться — плохо».", "I think “crying is weakness” or “being angry is bad”."), FREQ_R),
                    (("Yomon kayfiyat vaqtinchalik ekanini va o‘tib ketishini bilaman.", "Jaman kewil-kúydiń waqıtsha ekenin hám ótip ketetuǵının bilemen.", "Я знаю, что плохое настроение временно и пройдёт.", "I know a bad mood is temporary and will pass."), FREQ),
                ],
            },
            {
                "kind": "scenario",
                "title": ("Amaliy mashq: His-tuyg‘u nima demoqchi?", "Ámeliy shınıǵıw: Sezim ne demekshi?", "Практика: что говорит эмоция?", "Practice: what is the emotion saying?"),
                "body": SCENARIO_INTRO,
                "questions": [
                    (
                        ("Guruhdoshingiz siz bajargan ishni o‘ziniki qilib ko‘rsatdi. Sizda kuchli g‘azab paydo bo‘ldi.", "Toparlasıńız siz islegen jumıstı óziniki etip kórsetti. Sizde kúshli ashıw payda boldı.", "Одногруппник выдал вашу работу за свою. Вы почувствовали сильный гнев.", "A groupmate presented your work as their own. You feel strong anger."),
                        (
                            "G‘azabni yutib, hech narsa demayman | 0 | Bostirilgan g‘azab yo‘qolmaydi — u keyin charchoq yoki portlash bo‘lib qaytadi.\nUnga baqirib, hammaning oldida sharmanda qilaman | 1 | G‘azab energiyasi bor, lekin bu yo‘l nizoni kuchaytiradi.\nTinchlanib, unga va o‘qituvchiga ishning muallifi men ekanimni xotirjam aytaman | 2 | To‘g‘ri! G‘azab adolatsizlik signali — siz uning energiyasini o‘zingizni himoya qilishga yo‘naltirdingiz.",
                            "Ashıwdı jutıp, hesh nárse aytpayman | 0 | Basılǵan ashıw joǵalmaydı — ol keyin sharshaw yamasa jarılıw bolıp qaytadı.\nOǵan baqırıp, hámmeniń aldında masqara qılaman | 1 | Ashıwdıń energiyası bar, biraq bul jol kelispewshilikti kúsheytedi.\nTınıshlanıp, oǵan hám oqıtıwshıǵa jumıstıń avtorı men ekenimdi tınısh aytaman | 2 | Durıs! Ashıw — ádilsizlik signalı, siz onıń energiyasın ózińizdi qorǵawǵa baǵdarladıńız.",
                            "Проглочу гнев и ничего не скажу | 0 | Подавленный гнев не исчезает — он вернётся усталостью или вспышкой.\nНакричу на него и опозорю при всех | 1 | В гневе есть энергия, но так конфликт только усилится.\nУспокоюсь и спокойно скажу ему и преподавателю, что автор работы — я | 2 | Верно! Гнев — сигнал несправедливости, и вы направили его энергию на защиту себя.",
                            "Swallow the anger and say nothing | 0 | Suppressed anger doesn’t disappear — it comes back as exhaustion or an outburst.\nShout at them and shame them in front of everyone | 1 | Anger has energy, but this way only escalates the conflict.\nCalm down and calmly tell them and the teacher that I am the author | 2 | Right! Anger signals injustice — you used its energy to stand up for yourself.",
                        ),
                    ),
                    (
                        ("Yaqin do‘stingiz boshqa shaharga ko‘chib ketdi. Bir necha kundan beri qayg‘u his qilyapsiz.", "Jaqın dostıńız basqa qalaǵa kóship ketti. Bir neshe kúnnen beri qayǵı sezip atırsız.", "Близкий друг переехал в другой город. Несколько дней вы чувствуете грусть.", "A close friend moved to another city. You have felt sad for several days."),
                        (
                            "Qayg‘uni his qilishga o‘zimga ruxsat beraman va do‘stim bilan aloqani saqlash rejasini tuzaman | 2 | To‘g‘ri! Qayg‘u yo‘qotishni qayta ishlashga va nima qadrli ekanini anglashga yordam beradi.\n«Yig‘lamaslik kerak» deb o‘zimni majburan chalg‘itaman | 0 | Qayg‘udan qochish uni uzaytiradi va ijobiy his-tuyg‘ularni ham susaytiradi.\nHamma bilan aloqani uzib, uyda yolg‘iz o‘tiraman | 1 | Biroz yolg‘izlik normal, lekin uzoq izolyatsiya holatni og‘irlashtiradi.",
                            "Qayǵını seziwge ózime ruqsat beremen hám dostım menen baylanıstı saqlaw rejesin dúzemen | 2 | Durıs! Qayǵı joǵaltıwdı qayta islewge hám neniń qádirli ekenin túsiniwge járdem beredi.\n«Jılamaw kerek» dep ózimdi májbúrlep alańlataman | 0 | Qayǵıdan qashıw onı uzaytadı hám unamlı sezimlerdi de álsiretedi.\nHámme menen baylanıstı úzip, úyde jalǵız otıraman | 1 | Bir az jalǵızlıq qalıptı, biraq uzaq izolyaciya jaǵdaydı awırlastıradı.",
                            "Позволю себе грустить и составлю план, как поддерживать связь с другом | 2 | Верно! Грусть помогает пережить потерю и понять, что для вас ценно.\nБуду насильно отвлекаться: «плакать нельзя» | 0 | Бегство от грусти затягивает её и приглушает и радостные чувства.\nОтключусь от всех и буду сидеть дома один | 1 | Немного уединения — нормально, но долгая изоляция утяжеляет состояние.",
                            "Allow myself to feel sad and make a plan to stay in touch with my friend | 2 | Right! Sadness helps you process a loss and see what matters to you.\nForce myself to stay distracted: “I mustn’t cry” | 0 | Running from sadness prolongs it and dulls positive feelings too.\nCut off from everyone and sit at home alone | 1 | Some solitude is normal, but long isolation makes things heavier.",
                        ),
                    ),
                    (
                        ("Ertaga birinchi marta ko‘pchilik oldida taqdimot qilasiz. Qo‘rquv va hayajon kuchli.", "Erteń birinshi ret kópshilik aldında taqdimat qılasız. Qorqıw hám tolǵanıw kúshli.", "Завтра вы впервые выступаете с презентацией перед аудиторией. Страх и волнение сильные.", "Tomorrow you give your first presentation in front of many people. Fear and nerves are strong."),
                        (
                            "Qo‘rquvni signal deb qabul qilib, taqdimotni ikki marta mashq qilaman | 2 | Ajoyib! Qo‘rquv xavfni oldindan sezdiradi — siz uni yaxshiroq tayyorgarlikka aylantirdingiz.\nKasal bo‘ldim deb taqdimotga bormayman | 0 | Qochish bugun yengillik beradi, lekin keyingi safar qo‘rquv yanada kuchayadi.\nQo‘rquvni o‘ylamaslikka harakat qilaman, tayyorlanmayman | 1 | His-tuyg‘udan foydalanmaslik — uning xabarini e’tiborsiz qoldirish.",
                            "Qorqıwdı signal dep qabıllap, taqdimattı eki ret shınıqtıraman | 2 | Ájayıp! Qorqıw qáwipti aldınnan sezdiredi — siz onı jaqsıraq tayarlıqqa aylandırdıńız.\nAwırıp qaldım dep taqdimatqa barmayman | 0 | Qashıw búgin jeńillik beredi, biraq keyingi ret qorqıw jáne de kúsheyedi.\nQorqıw haqqında oylamawǵa háreket etemen, tayarlanbayman | 1 | Sezimnen paydalanbaw — onıń xabarın esapqa almaw.",
                            "Приму страх как сигнал и дважды отрепетирую выступление | 2 | Отлично! Страх предупреждает об опасности — вы превратили его в лучшую подготовку.\nСкажусь больным и не пойду | 0 | Избегание даёт облегчение сегодня, но в следующий раз страх станет сильнее.\nПостараюсь не думать о страхе и не буду готовиться | 1 | Не использовать эмоцию — значит игнорировать её сообщение.",
                            "Take the fear as a signal and rehearse the talk twice | 2 | Excellent! Fear warns of danger — you turned it into better preparation.\nSay I’m ill and skip it | 0 | Avoidance brings relief today, but next time the fear will be stronger.\nTry not to think about the fear and not prepare | 1 | Not using an emotion means ignoring its message.",
                        ),
                    ),
                ],
            },
            {
                "kind": "reflection",
                "title": ("O‘zingizga yordam: his-tuyg‘u kundaligi", "Ózińizge járdem: sezim kúndeligi", "Помоги себе: дневник эмоций", "Self-help: emotion diary"),
                "body": (
                    "Oxirgi kunlarda boshdan kechirgan bitta kuchli his-tuyg‘uni eslang. U qanday vaziyatda paydo bo‘ldi, tanangizda qanday sezildi va sizga qaysi ehtiyoj haqida xabar berdi?",
                    "Sońǵı kúnleri bastan keshirgen bir kúshli sezimdi eslań. Ol qanday jaǵdayda payda boldı, deneńizde qalay sezildi hám sizge qaysı mútájlik haqqında xabar berdi?",
                    "Вспомните одно сильное чувство последних дней. В какой ситуации оно появилось, как ощущалось в теле и о какой потребности сообщало?",
                    "Recall one strong feeling from the last few days. In what situation did it appear, how did it feel in your body, and which need was it telling you about?",
                ),
            },
        ],
    },
]


TOPICS_2 = [
    # ------------------------------------------------------------------ 3
    {
        "slug": "ei-3-self-awareness",
        "order": 3,
        "icon": "🪞",
        "color": "amber",
        "level": "beginner",
        "minutes": 15,
        "tags": "self-awareness, emotions, self-knowledge, confidence",
        "sources": (
            "Bradberry T., Greaves J. Emotional Intelligence 2.0. – San Diego: TalentSmart, 2009.\n"
            "Lemberg B. Emotsional intellekt: aql va his-tuyg‘ular o‘rtasidagi muloqot. – 2013.\n"
            "Mayer J. D., Salovey P., Caruso D. R. MSCEIT User’s Manual. – Toronto: MHS, 2002."
        ),
        "title": ("O‘z-o‘zini anglash", "Óz-ózin ańlaw", "Самоосознание", "Self-awareness"),
        "summary": (
            "His-tuyg‘ularingizni o‘sha zahoti sezish, ularning ildizini va takrorlanuvchi odatlaringizni topish.",
            "Sezimlerińizdi sol zamatta seziw, olardıń tamırın hám qaytalanatuǵın ádetlerińizdi tabıw.",
            "Замечать свои чувства в моменте, находить их причины и повторяющиеся привычки.",
            "Noticing your feelings in the moment and finding their roots and your recurring patterns.",
        ),
        "goal": (
            "His-tuyg‘ularingizni nomlash va ularning sababini topish odatini shakllantirasiz.",
            "Sezimlerińizdi ataw hám olardıń sebebin tabıw ádetin qáliplestiresiz.",
            "Вы выработаете привычку называть свои чувства и находить их причины.",
            "You will build the habit of naming your feelings and finding their causes.",
        ),
        "description": description(
            "O‘z-o‘zini anglash — hissiy intellektning poydevori. Bradberry va Greaves modelida u shaxs ichki kompetensiyaning birinchi ko‘nikmasi.",
            "Óz-ózin ańlaw — emocional intellekttiń tiykarı. Bradberry hám Greaves modelinde ol shaxs ishki kompetenciyasınıń birinshi kónlikpesi.",
            "Самоосознание — фундамент эмоционального интеллекта. В модели Брэдбери и Гривз это первый навык личностной компетенции.",
            "Self-awareness is the foundation of emotional intelligence. In the Bradberry–Greaves model it is the first skill of personal competence.",
        ),
        "steps": [
            {
                "kind": "lesson",
                "title": ("Ilmiy asos: o‘zingizni kuzatish", "Ilimiy tiykar: ózińizdi baqlaw", "Научная основа: наблюдать за собой", "Scientific basis: observing yourself"),
                "body": (
                    "T. Bradberry va J. Greaves (2009) hissiy intellektni to‘rt ko‘nikmaga ajratadi. Ikkitasi shaxs ichki (o‘z-o‘zini anglash, o‘z-o‘zini boshqarish), ikkitasi ijtimoiy (ijtimoiy ta’sirchanlik, munosabatlarni boshqarish). O‘z-o‘zini anglash — qolgan hammasining asosi.\n\n"
                    "Bu ko‘nikma uch narsani o‘z ichiga oladi: his-tuyg‘ularni o‘sha zahoti aniqlash, ularning manbasini tushunish va xulq-atvoringizdagi takrorlanuvchi odatlarni ko‘rish. His-tuyg‘u ko‘pincha «sababsiz» tuyulsa-da, aslida u har doim biror tajriba yoki vaziyatga bog‘liq.\n\n"
                    "Tana — eng yaxshi ko‘rsatkich. Yurak urishi, nafasning o‘zgarishi, mushaklarning taranglashuvi his-tuyg‘u kuchayayotganini ancha oldin bildiradi. B. Lemberg (2013) ta’kidlaydiki, ko‘pchilik o‘z his-tuyg‘ularini aniq ifodalashda qiynaladi — shuning uchun ularni so‘z bilan nomlashni o‘rganish kerak.\n\n"
                    "O‘zini yaxshi anglaydigan odamlar kuchli va zaif tomonlarini aniq biladi, nima ularni harakatga undashini tushunadi va xatolardan qo‘rqmaydi — ularni o‘rganish manbai deb qabul qiladi. Buning uchun o‘ziga nisbatan halollik kerak.",
                    "T. Bradberry hám J. Greaves (2009) emocional intellektti tórt kónlikpege bóledi. Ekewi shaxs ishki (óz-ózin ańlaw, óz-ózin basqarıw), ekewi social (social sezgirlik, qatnaslardı basqarıw). Óz-ózin ańlaw — qalǵanlarınıń hámmesiniń tiykarı.\n\n"
                    "Bul kónlikpe úsh nárseni óz ishine aladı: sezimlerdi sol zamatta anıqlaw, olardıń deregin túsiniw hám minez-qulqıńızdaǵı qaytalanatuǵın ádetlerdi kóriw. Sezim kóbinese «sebepsiz» bolıp kóringeni menen, ol hámme waqıt bir tájiriybe yamasa jaǵdayǵa baylanıslı.\n\n"
                    "Dene — eń jaqsı kórsetkish. Júrek urıwı, demniń ózgeriwi, bulshıq etlerdiń qısılıwı sezim kúsheyip atırǵanın ádewir aldın bildiredi. B. Lemberg (2013) atap ótkenindey, kópshilik óz sezimlerin anıq bildiriwde qıynaladı — sonlıqtan olardı sóz benen atawdı úyreniw kerek.\n\n"
                    "Ózin jaqsı ańlaytuǵın adamlar kúshli hám álsiz tárepin anıq biledi, olardı neniń háreketke iyteretuǵının túsinedi hám qátelerden qorıqpaydı — olardı úyreniw deregi dep qabıllaydı. Bunıń ushın ózine adalıq kerek.",
                    "Т. Брэдбери и Дж. Гривз (2009) делят эмоциональный интеллект на четыре навыка. Два личностных (самоосознание, самоуправление) и два социальных (социальная чуткость, управление отношениями). Самоосознание — основа всех остальных.\n\n"
                    "Этот навык включает три вещи: распознавать эмоции в момент их появления, понимать их источник и видеть повторяющиеся шаблоны в своём поведении. Хотя эмоция часто кажется «беспричинной», на деле она всегда связана с каким-то опытом или ситуацией.\n\n"
                    "Тело — лучший индикатор. Сердцебиение, изменение дыхания, напряжение мышц сообщают о нарастающей эмоции задолго до вспышки. Б. Лемберг (2013) отмечает, что большинству трудно точно выразить свои чувства, — поэтому нужно учиться называть их словами.\n\n"
                    "Люди с развитым самоосознанием точно знают свои сильные и слабые стороны, понимают, что их мотивирует, и не боятся ошибок — считают их источником роста. Для этого нужна честность с собой.",
                    "T. Bradberry and J. Greaves (2009) divide emotional intelligence into four skills: two personal (self-awareness, self-management) and two social (social awareness, relationship management). Self-awareness is the foundation of all the others.\n\n"
                    "It involves three things: recognising emotions as they happen, understanding where they come from and seeing the recurring patterns in your behaviour. An emotion may seem to come “out of nowhere”, but it is always linked to some experience or situation.\n\n"
                    "Your body is the best indicator. Heartbeat, changes in breathing and tense muscles signal a rising emotion long before it bursts out. B. Lemberg (2013) notes that most people struggle to express their feelings precisely — so we need to learn to name them in words.\n\n"
                    "Self-aware people know their strengths and weaknesses, understand what motivates them and are not afraid of mistakes — they treat them as a source of growth. This takes honesty with yourself.",
                ),
            },
            {
                "kind": "quiz",
                "title": ("Test: O‘zimni qanchalik anglayman?", "Test: Ózimdi qanshelli ańlayman?", "Тест: насколько я осознаю себя?", "Test: how self-aware am I?"),
                "body": TEST_INTRO,
                "results": (
                    (
                        "His-tuyg‘ularingiz ko‘pincha sizga «to‘satdan» keladi. Kuniga uch marta (ertalab, tushda, kechqurun) to‘xtab, «Hozir nimani his qilyapman va tanamda qayerda sezilyapti?» deb so‘rang.",
                        "Sezimlerińiz kóbinese sizge «tosınnan» keledi. Kúnine úsh ret (azanda, túste, keshte) toqtap, «Házir neni sezip atırman hám denemniń qay jerinde seziledi?» dep soraň.",
                        "Чувства часто застают вас «врасплох». Три раза в день (утром, днём, вечером) остановитесь и спросите: «Что я сейчас чувствую и где это в теле?»",
                        "Your feelings often catch you “by surprise”. Three times a day (morning, noon, evening) stop and ask: “What am I feeling now and where is it in my body?”",
                    ),
                    (
                        "Siz o‘zingizni ancha yaxshi kuzatasiz. Endi takrorlanuvchi odatlaringizga e’tibor bering: qaysi vaziyatlar sizni doim bir xil his-tuyg‘uga olib keladi?",
                        "Siz ózińizdi ádewir jaqsı baqlaysız. Endi qaytalanatuǵın ádetlerińizge dıqqat qaratıń: qaysı jaǵdaylar sizdi hámme waqıt bir qıylı sezimge alıp keledi?",
                        "Вы неплохо наблюдаете за собой. Теперь обратите внимание на повторяющиеся шаблоны: какие ситуации всегда вызывают у вас одно и то же чувство?",
                        "You observe yourself fairly well. Now look at your recurring patterns: which situations always lead you to the same feeling?",
                    ),
                    (
                        "Ajoyib! Siz o‘zingizni chuqur anglaysiz. Bu kuchingizdan qiyin vaziyatlarda o‘zingizni boshqarish uchun foydalaning — bu keyingi mavzu.",
                        "Ájayıp! Siz ózińizdi tereń ańlaysız. Bul kúshińizden qıyın jaǵdaylarda ózińizdi basqarıw ushın paydalanıń — bul keyingi tema.",
                        "Отлично! Вы глубоко осознаёте себя. Используйте эту силу, чтобы управлять собой в трудных ситуациях, — это следующая тема.",
                        "Excellent! You are deeply self-aware. Use this strength to manage yourself in hard situations — that’s the next topic.",
                    ),
                ),
                "questions": [
                    (("His-tuyg‘u kuchayayotganini tanamdagi belgilardan oldindan sezaman.", "Sezim kúsheyip atırǵanın denemdegi belgilerden aldınnan sezemen.", "Я заранее замечаю по телу, что эмоция нарастает.", "I notice from my body in advance that an emotion is rising."), FREQ),
                    (("His-tuyg‘ularimni bitta aniq so‘z bilan nomlay olaman (masalan, «xijolat», «hasad»).", "Sezimlerimdi bir anıq sóz benen atay alaman (mısalı, «uyalıw», «qızǵanısh»).", "Я могу назвать чувство одним точным словом (например, «неловкость», «зависть»).", "I can name a feeling with one precise word (e.g. “embarrassment”, “envy”)."), FREQ),
                    (("Qaysi vaziyatlar meni asabiylashtirishini bilaman.", "Qaysı jaǵdaylar meni ashıwlandıratuǵının bilemen.", "Я знаю, какие ситуации меня выводят из себя.", "I know which situations get on my nerves."), FREQ),
                    (("Kayfiyatim nega o‘zgarganini kun oxirigacha ham tushunmay qolaman.", "Kewil-kúyimniń ne ushın ózgergenin kún aqırına shekem de túsinbey qalaman.", "Я до вечера не понимаю, почему у меня испортилось настроение.", "Even by evening I don’t understand why my mood changed."), FREQ_R),
                    (("Xatolarimni o‘zim uchun saboq sifatida qabul qilaman.", "Qátelerimdi ózim ushın sabaq retinde qabıllayman.", "Я принимаю свои ошибки как урок для себя.", "I treat my mistakes as lessons for myself."), FREQ),
                ],
            },
            {
                "kind": "cards",
                "title": ("Amaliy mashq: His-tuyg‘u lug‘ati", "Ámeliy shınıǵıw: Sezim sózligi", "Практика: словарь эмоций", "Practice: the feelings dictionary"),
                "body": (
                    "Yurak tez uradi, kaftlar terlaydi | Xavotir yoki hayajon — «Meni nima kutyapti?» deb so‘rang\nJag‘ siqiladi, yuz qiziydi | G‘azab — «Qaysi chegaramni buzishdi?» deb so‘rang\nKo‘krakda og‘irlik, quvvat yo‘q | Qayg‘u — «Nimani yo‘qotdim?» deb so‘rang\nYuz qizaradi, ko‘zni olib qochgim keladi | Uyat yoki xijolat — «Kimning bahosidan qo‘rqyapman?» deb so‘rang\nKo‘krak kengayadi, jilmaygim keladi | Quvonch — «Buni yana nima qaytaradi?» deb so‘rang\n«Hammasi yomon» degan umumiy his | Aniqlashtiring: charchoq? xafagarchilik? yolg‘izlik?",
                    "Júrek tez soǵadı, alaqan terleydi | Tınıshsızlıq yamasa tolǵanıw — «Meni ne kútip tur?» dep soraň\nJaq qısıladı, júz qızadı | Ashıw — «Qaysı shegaramdı buzdı?» dep soraň\nKókirekte awırlıq, kúsh joq | Qayǵı — «Neni joǵalttım?» dep soraň\nJúz qızaradı, kózimdi alıp qashqım keledi | Uyat yamasa ıńǵaysızlıq — «Kimniń bahasınan qorqıp atırman?» dep soraň\nKókirek keńeyedi, kúlimsiregim keledi | Quwanısh — «Bunı jáne ne qaytaradı?» dep soraň\n«Hámmesi jaman» degen ulıwma sezim | Anıqlań: sharshaw? renjiw? jalǵızlıq?",
                    "Сердце колотится, ладони потеют | Тревога или волнение — спросите: «Что меня ждёт?»\nСжимается челюсть, горит лицо | Гнев — спросите: «Какую мою границу нарушили?»\nТяжесть в груди, нет сил | Грусть — спросите: «Что я потерял?»\nКраснею, хочется отвести глаза | Стыд или неловкость — спросите: «Чьей оценки я боюсь?»\nВ груди легко, хочется улыбаться | Радость — спросите: «Что ещё может это повторить?»\nОбщее «всё плохо» | Уточните: усталость? обида? одиночество?",
                    "Heart racing, sweaty palms | Anxiety or excitement — ask: “What is waiting for me?”\nJaw clenched, face hot | Anger — ask: “Which of my boundaries was crossed?”\nHeavy chest, no energy | Sadness — ask: “What have I lost?”\nBlushing, want to look away | Shame or embarrassment — ask: “Whose judgement am I afraid of?”\nLight chest, want to smile | Joy — ask: “What else could bring this back?”\nA vague “everything is bad” | Be precise: tiredness? hurt? loneliness?",
                ),
            },
            {
                "kind": "reflection",
                "title": ("O‘zingizga yordam: mening tetiklarim", "Ózińizge járdem: meniń qozǵawshılarım", "Помоги себе: мои триггеры", "Self-help: my triggers"),
                "body": (
                    "Sizni ko‘pincha asabiylashtiradigan yoki xafa qiladigan uchta vaziyatni yozing. Har birida tanangizda nima seziladi va keyingi safar buni sezganingizda o‘zingizga nima deysiz?",
                    "Sizdi kóbinese ashıwlandıratuǵın yamasa renjitetuǵın úsh jaǵdaydı jazıń. Hár birinde deneńizde ne seziledi hám keyingi ret bunı sezgenińizde ózińizge ne deysiz?",
                    "Запишите три ситуации, которые чаще всего вас злят или расстраивают. Что в каждой из них вы чувствуете в теле и что скажете себе, когда заметите это в следующий раз?",
                    "Write down three situations that most often anger or upset you. What do you feel in your body in each, and what will you tell yourself next time you notice it?",
                ),
            },
        ],
    },
    # ------------------------------------------------------------------ 4
    {
        "slug": "ei-4-self-management-and-stress",
        "order": 4,
        "icon": "🌿",
        "color": "mint",
        "level": "intermediate",
        "minutes": 20,
        "tags": "self-management, stress, breathing, calm",
        "sources": (
            "Bradberry T., Greaves J. Emotional Intelligence 2.0. – San Diego: TalentSmart, 2009.\n"
            "Lemberg B. Emotsional intellekt: aql va his-tuyg‘ular o‘rtasidagi muloqot. – 2013.\n"
            "Gross J. J. The emerging field of emotion regulation: An integrative review // Review of General Psychology. – 1998. – Vol. 2(3). – P. 271–299.\n"
            "Goleman D. Emotional Intelligence: Why It Can Matter More Than IQ. – New York: Bantam Books, 1995."
        ),
        "title": ("O‘zini boshqarish va stress", "Ózin basqarıw hám stress", "Самоуправление и стресс", "Self-management and stress"),
        "summary": (
            "«Qochish, kurashish, muzlash» reaksiyasi, impulslarni nazorat qilish va stressni tez pasaytirish usullari.",
            "«Qashıw, gúresiw, qatıp qalıw» reakciyası, impulslardı qadaǵalaw hám stressti tez páseytiw usılları.",
            "Реакция «бей, беги, замри», контроль импульсов и способы быстро снизить стресс.",
            "The fight–flight–freeze reaction, impulse control and quick ways to lower stress.",
        ),
        "goal": (
            "Stress paytida o‘zingizni tinchlantiradigan shaxsiy usulingizni topasiz va impulsiv reaksiyalarni to‘xtatishni o‘rganasiz.",
            "Stress waqtında ózińizdi tınıshlandıratuǵın jeke usılıńızdı tabasız hám impulsiv reakciyalardı toqtatıwdı úyrenesiz.",
            "Вы найдёте свой личный способ успокаиваться в стрессе и научитесь останавливать импульсивные реакции.",
            "You will find your personal way to calm down under stress and learn to stop impulsive reactions.",
        ),
        "description": description(
            "O‘z-o‘zini boshqarish — his-tuyg‘ularni bostirish emas, ularni anglagan holda to‘g‘ri harakatni tanlash. Lemberg fikricha, stressni boshqarmasdan turib his-tuyg‘ularni nazorat qilib bo‘lmaydi.",
            "Óz-ózin basqarıw — sezimlerdi basıw emes, olardı ańlaǵan halda durıs háreketti tańlaw. Lemberg pikirinshe, stressti basqarmay turıp sezimlerdi qadaǵalaw múmkin emes.",
            "Самоуправление — это не подавление чувств, а осознанный выбор правильного действия. По Лембергу, без управления стрессом невозможно контролировать эмоции.",
            "Self-management is not suppressing feelings but consciously choosing the right action. According to Lemberg, you can’t control emotions without managing stress.",
        ),
        "steps": [
            {
                "kind": "lesson",
                "title": ("Ilmiy asos: stress va miya", "Ilimiy tiykar: stress hám miy", "Научная основа: стресс и мозг", "Scientific basis: stress and the brain"),
                "body": (
                    "Axborot juda kuchli yoki stressli bo‘lsa, miyada instinktiv mexanizmlar ustunlik qiladi va xatti-harakat uch reaksiyaga torayadi: qochish, kurashish yoki muzlash. Bunday paytda aniq fikrlash qiyinlashadi. B. Lemberg (2013) yozadi: stressni boshqarmasdan turib inson o‘z his-tuyg‘ularini nazorat qila olmaydi.\n\n"
                    "Bradberry va Greaves (2009) bo‘yicha o‘z-o‘zini boshqarish — impulslarni nazorat qilish, stressda barqaror qolish va uzoq muddatli maqsad uchun qisqa muddatli reaksiyani cheklash. Bu bostirish emas: J. Gross (1998) ko‘rsatganidek, bostirish zarar keltiradi. Gap his-tuyg‘uni anglab, moslashuvchan harakatni ongli tanlashda.\n\n"
                    "Stressni pasaytirish uch bosqichda: 1) stressni tan olish — mushaklar taranglashuvi, nafasning tezlashuvini sezish; 2) o‘z reaksiyangizni bilish — asabiylashuvga moyil odamga tinchlantiruvchi, so‘lg‘inlikka moyil odamga faollashtiruvchi usullar kerak; 3) mos usulni tanlash.\n\n"
                    "Eng samarali usul — kamida bitta sezgi kanalini ishga solish: ko‘rish (tabiat manzarasi), eshitish (sevimli musiqa), hid (choy, atir), teginish (iliq suv, mushuk), ta’m (yalpiz). Har kimning usuli o‘ziga xos — uni tajriba orqali topasiz. Sekin nafas olish ham asab tizimini tinchlantiradi.",
                    "Maǵlıwmat júdá kúshli yamasa stressli bolsa, miyda instinktiv mexanizmler ústemlik etedi hám minez-qulıq úsh reakciyaǵa tarayadı: qashıw, gúresiw yamasa qatıp qalıw. Bunday waqıtta anıq oylaw qıyınlasadı. B. Lemberg (2013) jazadı: stressti basqarmay turıp adam óz sezimlerin qadaǵalay almaydı.\n\n"
                    "Bradberry hám Greaves (2009) boyınsha óz-ózin basqarıw — impulslardı qadaǵalaw, stresste turaqlı qalıw hám uzaq múddetli maqset ushın qısqa múddetli reakciyanı sheklew. Bul basıw emes: J. Gross (1998) kórsetkenindey, basıw ziyan keltiredi. Gáp sezimdi ańlap, beyimlesiwshi háreketti sanalı tańlawda.\n\n"
                    "Stressti páseytiw úsh basqıshta: 1) stressti moyınlaw — bulshıq etlerdiń qısılıwın, demniń tezlesiwin seziw; 2) óz reakciyańızdı biliw — ashıwlanıwǵa beyim adamǵa tınıshlandırıwshı, solǵınlıqqa beyim adamǵa belsendilendiriwshi usıllar kerek; 3) say usıldı tańlaw.\n\n"
                    "Eń nátiyjeli usıl — keminde bir sezim kanalın iske qosıw: kóriw (tábiyat kórinisi), esitiw (súyikli muzıka), iyis (shay, átir), tiyiw (jıllı suw, pıshıq), dám (jalbız). Hárkimniń usılı ózine tán — onı tájiriybe arqalı tabasız. Áste dem alıw da nerv sistemasın tınıshlandıradı.",
                    "Когда информация слишком сильная или стрессовая, в мозге берут верх инстинктивные механизмы, и поведение сужается до трёх реакций: бей, беги или замри. В такой момент ясно думать трудно. Б. Лемберг (2013) пишет: не управляя стрессом, человек не может контролировать свои эмоции.\n\n"
                    "По Брэдбери и Гривз (2009), самоуправление — это контроль импульсов, устойчивость в стрессе и отказ от сиюминутной реакции ради долгосрочной цели. Это не подавление: как показал Дж. Гросс (1998), подавление вредит. Суть — осознать эмоцию и сознательно выбрать гибкое действие.\n\n"
                    "Снижение стресса — в три шага: 1) признать стресс — заметить напряжение мышц, учащённое дыхание; 2) знать свою реакцию — тому, кто склонен к возбуждению, нужны успокаивающие способы, тому, кто склонен к апатии, — активирующие; 3) подобрать подходящий способ.\n\n"
                    "Самый действенный способ — задействовать хотя бы один канал чувств: зрение (вид природы), слух (любимая музыка), обоняние (чай, духи), осязание (тёплая вода, кошка), вкус (мята). У каждого свой способ — его находят на практике. Медленное дыхание тоже успокаивает нервную систему.",
                    "When information is too intense or stressful, instinctive mechanisms take over the brain and behaviour narrows to three reactions: fight, flight or freeze. In that moment clear thinking is hard. B. Lemberg (2013) writes that without managing stress a person cannot control their emotions.\n\n"
                    "For Bradberry and Greaves (2009), self-management means controlling impulses, staying steady under stress and holding back a momentary reaction for a long-term goal. It is not suppression: James Gross (1998) showed suppression does harm. The point is to recognise the emotion and consciously choose a flexible action.\n\n"
                    "Lowering stress takes three steps: 1) admit the stress — notice tense muscles, faster breathing; 2) know your reaction — people prone to agitation need calming methods, people prone to shutting down need energising ones; 3) pick a method that fits.\n\n"
                    "The most effective method engages at least one sense: sight (a view of nature), hearing (favourite music), smell (tea, perfume), touch (warm water, a cat), taste (mint). Everyone’s method is different — you find yours through practice. Slow breathing also calms the nervous system.",
                ),
            },
            {
                "kind": "quiz",
                "title": ("Test: Stressda o‘zimni qanday tutaman?", "Test: Stresste ózimdi qalay tutaman?", "Тест: как я веду себя в стрессе?", "Test: how do I handle stress?"),
                "body": TEST_INTRO,
                "results": (
                    (
                        "Stress sizni tez-tez «egallab oladi». Bu xavfli emas, lekin charchatadi. Har kuni 3 daqiqa sekin nafas mashqini bajaring va o‘zingizga mos «sezgi usuli»ni toping (keyingi qadamda).",
                        "Stress sizdi jiyi-jiyi «iyelep aladı». Bul qáwipli emes, biraq sharshatadı. Hár kúni 3 minut áste dem alıw shınıǵıwın orınlań hám ózińizge say «sezim usılın» tabıń (keyingi qádemde).",
                        "Стресс часто «захватывает» вас. Это не опасно, но выматывает. Делайте каждый день 3 минуты медленного дыхания и найдите свой «сенсорный способ» (на следующем шаге).",
                        "Stress often “takes over” you. It isn’t dangerous, but it’s draining. Do 3 minutes of slow breathing every day and find your own “sensory method” (next step).",
                    ),
                    (
                        "Ko‘p hollarda o‘zingizni boshqarasiz. Eng qiyin vaziyatlar uchun oldindan reja tuzing: «Jahlim chiqsa, avval 10 gacha sanayman va nafas olaman».",
                        "Kóp jaǵdaylarda ózińizdi basqarasız. Eń qıyın jaǵdaylar ushın aldınnan reje dúziń: «Ashıwım kelse, aldın 10 ǵa shekem sanayman hám dem alaman».",
                        "Чаще всего вы управляете собой. Составьте заранее план для самых трудных ситуаций: «Если разозлюсь — сначала досчитаю до 10 и сделаю вдох».",
                        "Most of the time you manage yourself. Make a plan in advance for the hardest moments: “If I get angry, I’ll count to 10 and breathe first.”",
                    ),
                    (
                        "Ajoyib! Siz stressda ham barqaror qolasiz. Bu tajribangiz bilan atrofingizdagilarga ham yordam bera olasiz.",
                        "Ájayıp! Siz stresste de turaqlı qalasız. Bul tájiriybeńiz benen átirapıńızdaǵılarǵa da járdem bere alasız.",
                        "Отлично! Вы сохраняете устойчивость и в стрессе. Этим опытом вы можете помогать и окружающим.",
                        "Excellent! You stay steady even under stress. You can use this to help people around you too.",
                    ),
                ),
                "questions": [
                    (("Jahlim chiqsa, keyin afsuslanadigan gaplarni aytib yuboraman.", "Ashıwım kelse, keyin ókinetuǵın sózlerdi aytıp jiberemen.", "Когда я злюсь, говорю то, о чём потом жалею.", "When angry, I say things I later regret."), FREQ_R),
                    (("Stressni tanamdagi belgilardan (taranglik, tez nafas) sezaman.", "Stressti denemdegi belgilerden (qısılıw, tez dem) sezemen.", "Я замечаю стресс по телу (напряжение, частое дыхание).", "I notice stress through my body (tension, fast breathing)."), FREQ),
                    (("Meni tez tinchlantiradigan aniq usulim bor.", "Meni tez tınıshlandıratuǵın anıq usılım bar.", "У меня есть способ, который быстро меня успокаивает.", "I have a specific way that calms me down quickly."), FREQ),
                    (("Qiyin vaziyatda «muzlab» qolaman va hech narsa qila olmayman.", "Qıyın jaǵdayda «qatıp» qalaman hám hesh nárse isley almayman.", "В трудной ситуации я «замираю» и ничего не могу сделать.", "In a hard situation I “freeze” and can’t do anything."), FREQ_R),
                    (("Uzoq muddatli maqsad uchun hozirgi istakdan voz kecha olaman.", "Uzaq múddetli maqset ushın házirgi qálewden waz kese alaman.", "Ради долгосрочной цели я могу отказаться от сиюминутного желания.", "I can give up a momentary urge for a long-term goal."), FREQ),
                ],
            },
            {
                "kind": "breathing",
                "title": ("Amaliy mashq: Tinchlantiruvchi nafas", "Ámeliy shınıǵıw: Tınıshlandırıwshı dem", "Практика: успокаивающее дыхание", "Practice: calming breath"),
                "body": (
                    "Qulay o‘tiring. Doira kattalashganda burun orqali nafas oling, to‘xtaganda ushlab turing, kichrayganda og‘iz orqali sekin chiqaring. Nafas chiqarish olishdan uzunroq — bu asab tizimini tinchlantiradi.",
                    "Qolaylı otırıń. Sheńber úlkeygende murın arqalı dem alıń, toqtaǵanda uslap turıń, kishireygende awız arqalı áste shıǵarıń. Dem shıǵarıw alıwdan uzınıraq — bul nerv sistemasın tınıshlandıradı.",
                    "Сядьте удобно. Когда круг растёт — вдох через нос, когда замирает — задержка, когда уменьшается — медленный выдох через рот. Выдох длиннее вдоха — это успокаивает нервную систему.",
                    "Sit comfortably. As the circle grows, breathe in through your nose; when it pauses, hold; as it shrinks, breathe out slowly through your mouth. A longer out-breath calms the nervous system.",
                ),
                "breathing": (4, 2, 6, 5),
            },
            {
                "kind": "reflection",
                "title": ("O‘zingizga yordam: stressga qarshi rejam", "Ózińizge járdem: stresske qarsı rejem", "Помоги себе: мой антистресс-план", "Self-help: my anti-stress plan"),
                "body": (
                    "Beshta sezgidan (ko‘rish, eshitish, hid, teginish, ta’m) har biri uchun sizni tinchlantiradigan bitta narsani yozing. Keyingi stressli vaziyatda qaysi birini birinchi qo‘llaysiz?",
                    "Bes sezimniń (kóriw, esitiw, iyis, tiyiw, dám) hár biri ushın sizdi tınıshlandıratuǵın bir nárseni jazıń. Keyingi stressli jaǵdayda qaysısın birinshi qollanasız?",
                    "Для каждого из пяти чувств (зрение, слух, обоняние, осязание, вкус) запишите одну вещь, которая вас успокаивает. Что вы примените первым в следующей стрессовой ситуации?",
                    "For each of the five senses (sight, hearing, smell, touch, taste) write one thing that calms you. Which will you use first in your next stressful situation?",
                ),
            },
        ],
    },
    # ------------------------------------------------------------------ 5
    {
        "slug": "ei-5-empathy-and-social-awareness",
        "order": 5,
        "icon": "🤝",
        "color": "ocean",
        "level": "intermediate",
        "minutes": 15,
        "tags": "empathy, social awareness, nonverbal, communication",
        "sources": (
            "Bradberry T., Greaves J. Emotional Intelligence 2.0. – San Diego: TalentSmart, 2009.\n"
            "Rizzolatti G., Craighero L. The mirror-neuron system // Annual Review of Neuroscience. – 2004. – Vol. 27. – P. 169–192.\n"
            "Lemberg B. Emotsional intellekt: aql va his-tuyg‘ular o‘rtasidagi muloqot. – 2013.\n"
            "Gardner H. Frames of Mind: The Theory of Multiple Intelligences. – New York: Basic Books, 1983."
        ),
        "title": ("Empatiya va ijtimoiy ta’sirchanlik", "Empatiya hám social sezgirlik", "Эмпатия и социальная чуткость", "Empathy and social awareness"),
        "summary": (
            "Boshqalarning his-tuyg‘ularini yuz ifodasi, ovoz va tana tilidan o‘qish va ularning ehtiyojini tushunish.",
            "Basqalardıń sezimlerin júz kórinisi, dawıs hám dene tilinen oqıw hám olardıń mútájligin túsiniw.",
            "Читать чувства других по лицу, голосу и языку тела и понимать их потребности.",
            "Reading other people’s feelings from their face, voice and body language and understanding their needs.",
        ),
        "goal": (
            "Suhbatdoshning noverbal signallarini sezish va unga hamdardlik bilan javob berishni o‘rganasiz.",
            "Sáwbetlesiwshiniń noverbal signalların seziw hám oǵan hamdardlıq penen juwap beriwdi úyrenesiz.",
            "Вы научитесь замечать невербальные сигналы собеседника и отвечать ему с сочувствием.",
            "You will learn to notice others’ nonverbal signals and respond with compassion.",
        ),
        "description": description(
            "Ijtimoiy ta’sirchanlik — hissiy intellektning birinchi shaxslararo ko‘nikmasi. Uning miya asosi — «ko‘zgu neyronlar».",
            "Social sezgirlik — emocional intellekttiń birinshi shaxslar aralıq kónlikpesi. Onıń miy tiykarı — «ayna neyronlar».",
            "Социальная чуткость — первый межличностный навык эмоционального интеллекта. Её мозговая основа — «зеркальные нейроны».",
            "Social awareness is the first interpersonal skill of emotional intelligence. Its brain basis is “mirror neurons”.",
        ),
        "steps": [
            {
                "kind": "lesson",
                "title": ("Ilmiy asos: boshqalarni his qilish", "Ilimiy tiykar: basqalardı seziw", "Научная основа: чувствовать других", "Scientific basis: feeling others"),
                "body": (
                    "Ijtimoiy ta’sirchanlik — boshqa insonlarning hissiy holatini anglash va tushunish qobiliyati. U empatiyani, ijtimoiy signallarni idrok etishni va boshqalarning motiv hamda ehtiyojlarini tushunishni o‘z ichiga oladi (Bradberry & Greaves, 2009).\n\n"
                    "Bunda «ko‘zgu neyronlar» muhim rol o‘ynaydi: ular inson o‘zi biror his-tuyg‘uni boshdan kechirganda ham, boshqada shu his-tuyg‘uni ko‘rganda ham bir xil faollashadi. Shuning uchun biz yig‘layotgan odamni ko‘rib, o‘zimiz ham ma’yus tortamiz.\n\n"
                    "Muloqotda axborotning katta qismi so‘z orqali emas, noverbal yo‘l bilan uzatiladi: ovoz ohangi, yuz ifodasi, tana holati, imo-ishoralar va ko‘z bilan aloqa. Ko‘pincha odamning tana tili aytgan so‘zlaridan ko‘ra ko‘proq narsani bildiradi.\n\n"
                    "Boshqalarni yaxshi tushunish uchun o‘z ichki monologingizni vaqtincha to‘xtatib, e’tiborni suhbatdoshga qaratish kerak. Bu antropolog kuzatuviga o‘xshaydi: vaziyatni xolis ko‘rish va o‘z his-tuyg‘ularingiz idrokka aralashmasligiga harakat qilish.",
                    "Social sezgirlik — basqa adamlardıń sezimlik halın ańlaw hám túsiniw qábileti. Ol empatiyanı, social signallardı qabıllawdı hám basqalardıń motivi menen mútájliklerin túsiniwdi óz ishine aladı (Bradberry & Greaves, 2009).\n\n"
                    "Bunda «ayna neyronlar» áhmiyetli rol oynaydı: olar adam ózi bir sezimdi bastan keshirgende de, basqada sol sezimdi kórgende de birdey belsendi boladı. Sonlıqtan biz jılap atırǵan adamdı kórip, ózimiz de muńayıp qalamız.\n\n"
                    "Qarım-qatnasta maǵlıwmattıń úlken bólegi sóz arqalı emes, noverbal jol menen beriledi: dawıs ırǵaǵı, júz kórinisi, dene halatı, ım-isharalar hám kóz benen baylanıs. Kóbinese adamnıń dene tili aytqan sózlerinen kóbirek nárseni bildiredi.\n\n"
                    "Basqalardı jaqsı túsiniw ushın óz ishki monologıńızdı waqıtsha toqtatıp, dıqqattı sáwbetlesiwshige qaratıw kerek. Bul antropolog baqlawına uqsaydı: jaǵdaydı xolıs kóriw hám óz sezimlerińiz qabıllawǵa aralaspawına háreket etiw.",
                    "Социальная чуткость — способность осознавать и понимать эмоциональное состояние других людей. Она включает эмпатию, восприятие социальных сигналов и понимание мотивов и потребностей других (Брэдбери и Гривз, 2009).\n\n"
                    "Важную роль играют «зеркальные нейроны»: они одинаково активируются, когда человек сам испытывает эмоцию и когда видит её у другого. Поэтому, глядя на плачущего человека, мы и сами грустнеем.\n\n"
                    "Большая часть информации в общении передаётся не словами, а невербально: тоном голоса, мимикой, позой, жестами и взглядом. Часто язык тела говорит о человеке больше, чем его слова.\n\n"
                    "Чтобы хорошо понимать других, нужно на время остановить свой внутренний монолог и направить внимание на собеседника. Это похоже на наблюдение антрополога: видеть ситуацию объективно и не давать своим эмоциям искажать восприятие.",
                    "Social awareness is the ability to recognise and understand other people’s emotional states. It includes empathy, picking up social signals and understanding others’ motives and needs (Bradberry & Greaves, 2009).\n\n"
                    "“Mirror neurons” play a key role: they fire both when we feel an emotion ourselves and when we see it in someone else. That’s why watching someone cry makes us sad too.\n\n"
                    "Most information in conversation is carried not by words but nonverbally: tone of voice, facial expression, posture, gestures and eye contact. A person’s body language often says more than their words.\n\n"
                    "To understand others well, pause your inner monologue for a while and turn your attention to the other person. It is like an anthropologist’s observation: seeing the situation objectively and not letting your own feelings distort what you perceive.",
                ),
            },
            {
                "kind": "quiz",
                "title": ("Test: Empatiya darajam", "Test: Empatiya dárejem", "Тест: мой уровень эмпатии", "Test: my level of empathy"),
                "body": TEST_INTRO,
                "results": (
                    (
                        "Boshqalarning his-tuyg‘ularini sezish hozircha qiyin. Bugundan har bir suhbatda o‘zingizdan so‘rang: «U hozir nimani his qilyapti va bu uning yuzida qanday ko‘rinyapti?»",
                        "Basqalardıń sezimlerin seziw házirshe qıyın. Búginnen baslap hár bir sáwbette ózińizden soraň: «Ol házir neni sezip atır hám bul onıń júzinde qalay kórinip tur?»",
                        "Пока вам трудно замечать чувства других. С сегодняшнего дня в каждом разговоре спрашивайте себя: «Что он сейчас чувствует и как это видно по его лицу?»",
                        "Noticing others’ feelings is still hard for you. From today, in every conversation ask yourself: “What is this person feeling now, and how does it show on their face?”",
                    ),
                    (
                        "Siz boshqalarni ancha yaxshi tushunasiz. Endi his-tuyg‘uni sezgan paytingizda uni ovoz chiqarib aytishni mashq qiling: «Charchagan ko‘rinasan, hammasi joyidami?»",
                        "Siz basqalardı ádewir jaqsı túsinesiz. Endi sezimdi sezgen waqtıńızda onı dawıs shıǵarıp aytıwdı shınıqtırıń: «Sharshaǵan kórinesiń, hámmesi jaqsı ma?»",
                        "Вы неплохо понимаете других. Теперь тренируйтесь называть замеченное чувство вслух: «Ты выглядишь уставшим, всё в порядке?»",
                        "You understand others fairly well. Now practise naming the feeling you notice out loud: “You look tired — is everything OK?”",
                    ),
                    (
                        "Ajoyib! Siz yuqori empatiyaga egasiz. Faqat boshqalarning his-tuyg‘ulari sizni haddan tashqari charchatmasligi uchun o‘zingizga ham g‘amxo‘rlik qiling.",
                        "Ájayıp! Sizde joqarı empatiya bar. Tek basqalardıń sezimleri sizdi tım sharshatpawı ushın ózińizge de ǵamxorlıq etiń.",
                        "Отлично! У вас высокая эмпатия. Только заботьтесь и о себе, чтобы чужие эмоции вас не выматывали.",
                        "Excellent! You have high empathy. Just take care of yourself too, so others’ emotions don’t drain you.",
                    ),
                ),
                "questions": [
                    (("Do‘stim «hammasi yaxshi» desa ham, aslida xafa ekanini sezaman.", "Dostım «hámmesi jaqsı» dese de, shınında renjigenin sezemen.", "Даже если друг говорит «всё хорошо», я чувствую, что он расстроен.", "Even when a friend says “I’m fine”, I sense they’re upset."), FREQ),
                    (("Suhbat paytida odamning yuz ifodasi va ovoziga e’tibor beraman.", "Sáwbet waqtında adamnıń júz kórinisi hám dawısına dıqqat qaratamın.", "Во время разговора я обращаю внимание на мимику и голос человека.", "During conversations I pay attention to people’s faces and voices."), FREQ),
                    (("Birov o‘z muammosini aytsa, darhol o‘z hikoyamni gapira boshlayman.", "Birew óz máselesin aytsa, dárhal óz gúrrińimdi aytıp baslayman.", "Когда кто-то рассказывает о проблеме, я сразу начинаю говорить о своём.", "When someone shares a problem, I immediately start talking about mine."), FREQ_R),
                    (("O‘zimni boshqa odamning o‘rniga qo‘yib ko‘raman.", "Ózimdi basqa adamnıń ornına qoyıp kóremen.", "Я ставлю себя на место другого человека.", "I put myself in the other person’s shoes."), FREQ),
                    (("Odamlarning xatti-harakati ortidagi sababni tushunishga harakat qilaman.", "Adamlardıń háreketiniń artındaǵı sebepti túsiniwge háreket etemen.", "Я стараюсь понять причину поступков людей.", "I try to understand the reasons behind people’s behaviour."), FREQ),
                ],
            },
            {
                "kind": "cards",
                "title": ("Amaliy mashq: Tana tilini o‘qish", "Ámeliy shınıǵıw: Dene tilin oqıw", "Практика: читаем язык тела", "Practice: reading body language"),
                "body": (
                    "Qo‘llar ko‘krakda chalishtirilgan, tana orqaga tortilgan | Himoyalanish yoki noqulaylik — bosimni kamaytiring, ochiq savol bering\nKo‘z qochiriladi, ovoz past | Xijolat yoki qo‘rquv — xavfsiz muhit yarating, shoshirmang\nTez gapiradi, qo‘llari tinim bilmaydi | Hayajon yoki xavotir — tinch ohangda gapiring\nYelkalar tushgan, nigoh pastda | Charchoq yoki qayg‘u — «Yordam kerakmi?» deb so‘rang\nOldinga engashgan, bosh irg‘ab turadi | Qiziqish va ishonch — suhbatni davom ettiring\nSo‘zlar «yaxshi», lekin yuzda tabassum yo‘q | So‘z va tana mos emas — tana tiliga ko‘proq ishoning, ehtiyotkorlik bilan so‘rang",
                    "Qollar kókirekte aykastırılǵan, dene artqa tartılǵan | Qorǵanıw yamasa ıńǵaysızlıq — basımdı azaytıń, ashıq soraw beriń\nKóz qashırıladı, dawıs páste | Uyalıw yamasa qorqıw — qáwipsiz ortalıq jaratıń, asıqtırmań\nTez sóyleydi, qolları tınım bilmeydi | Tolǵanıw yamasa tınıshsızlıq — tınısh dawıs penen sóyleń\nIyinler túsken, kózi tómende | Sharshaw yamasa qayǵı — «Járdem kerek pe?» dep soraň\nAldıǵa eńkeygen, bas iyzep turadı | Qızıǵıwshılıq hám isenim — sáwbetti dawam etiń\nSózler «jaqsı», biraq júzinde kúlki joq | Sóz benen dene say emes — dene tiline kóbirek iseniń, abaylap soraň",
                    "Руки скрещены на груди, корпус отклонён назад | Защита или дискомфорт — снизьте давление, задайте открытый вопрос\nОтводит взгляд, тихий голос | Смущение или страх — создайте безопасную обстановку, не торопите\nГоворит быстро, руки не находят места | Волнение или тревога — говорите спокойным тоном\nПлечи опущены, взгляд вниз | Усталость или грусть — спросите: «Тебе нужна помощь?»\nНаклонился вперёд, кивает | Интерес и доверие — продолжайте разговор\nСлова «хорошо», но на лице нет улыбки | Слова и тело не совпадают — больше верьте телу, бережно уточните",
                    "Arms crossed, body leaning back | Defensiveness or discomfort — lower the pressure, ask an open question\nAvoiding eye contact, quiet voice | Embarrassment or fear — create a safe space, don’t rush\nTalking fast, restless hands | Excitement or anxiety — speak in a calm tone\nShoulders dropped, eyes down | Tiredness or sadness — ask: “Do you need help?”\nLeaning forward, nodding | Interest and trust — keep the conversation going\nSays “fine” but no smile | Words and body don’t match — trust the body more, ask gently",
                ),
            },
            {
                "kind": "reflection",
                "title": ("O‘zingizga yordam: boshqaning ko‘zi bilan", "Ózińizge járdem: basqanıń kózi menen", "Помоги себе: глазами другого", "Self-help: through someone else’s eyes"),
                "body": (
                    "Yaqinda kimdir bilan kelishmovchilik bo‘lgan vaziyatni eslang. O‘sha odam nimani his qilgan bo‘lishi mumkin va uning qaysi ehtiyoji qondirilmagan edi? Endi uni qanday tushunasiz?",
                    "Jaqında birew menen kelispewshilik bolǵan jaǵdaydı eslań. Sol adam neni sezgen bolıwı múmkin hám onıń qaysı mútájligi qanaatlandırılmaǵan edi? Endi onı qalay túsinesiz?",
                    "Вспомните недавнее разногласие с кем-то. Что мог чувствовать этот человек и какая его потребность не была удовлетворена? Как вы понимаете его теперь?",
                    "Recall a recent disagreement with someone. What might that person have felt, and which of their needs wasn’t met? How do you understand them now?",
                ),
            },
        ],
    },
]


TOPICS_3 = [
    # ------------------------------------------------------------------ 6
    {
        "slug": "ei-6-mindful-listening",
        "order": 6,
        "icon": "👂",
        "color": "violet",
        "level": "intermediate",
        "minutes": 20,
        "tags": "listening, empathy, communication, mindfulness",
        "sources": (
            "Su A. J., Wilkins M. M. Barriers to listening // HBR Guide to Better Listening. – Boston: Harvard Business Review Press, 2020.\n"
            "Nichols R. G., Stevens L. A. Listening to people // HBR Guide to Better Listening. – Boston: Harvard Business Review Press, 2020.\n"
            "Riordan C. M. Three ways leaders can listen with more empathy // HBR Guide to Better Listening. – Boston: Harvard Business Review Press, 2020.\n"
            "Hougaard R., Carter J. Presence: the key to listening // HBR Guide to Better Listening. – Boston: Harvard Business Review Press, 2020.\n"
            "Groysberg B., Slind M. Talk, Inc. – Boston: Harvard Business Review Press, 2012."
        ),
        "title": ("Ongli tinglash: ichki to‘siqlar va filtrlar", "Sanalı tıńlaw: ishki tosıqlar hám filtrler", "Осознанное слушание: внутренние барьеры и фильтры", "Mindful listening: inner barriers and filters"),
        "summary": (
            "Ichki tanqidchi, oldindan javob tayyorlash, tasdiqlovchi og‘ish va empatik tinglashning uch qadami.",
            "Ishki sınshı, aldınnan juwap tayarlaw, tastıyıqlawshı awıwshılıq hám empatik tıńlawdıń úsh qádemi.",
            "Внутренний критик, подготовка ответа заранее, предвзятость подтверждения и три шага эмпатического слушания.",
            "The inner critic, preparing your reply too early, confirmation bias and three steps of empathic listening.",
        ),
        "goal": (
            "Tinglashga xalaqit beradigan o‘z to‘siqlaringizni taniysiz va suhbatdoshni to‘liq e’tibor bilan tinglashni o‘rganasiz.",
            "Tıńlawǵa kesent beretuǵın óz tosıqlarıńızdı tanıysız hám sáwbetlesiwshini tolıq dıqqat penen tıńlawdı úyrenesiz.",
            "Вы узнаете свои барьеры слушания и научитесь слушать собеседника с полным вниманием.",
            "You will recognise your own listening barriers and learn to listen with full attention.",
        ),
        "description": description(
            "Harvard Business Review tadqiqotlariga ko‘ra, tinglashdagi asosiy muammolar tashqi emas, balki ichki — kognitiv va emotsional to‘siqlar.",
            "Harvard Business Review izertlewlerine qaraǵanda, tıńlawdaǵı tiykarǵı máseleler sırtqı emes, al ishki — kognitiv hám sezimlik tosıqlar.",
            "По исследованиям Harvard Business Review, главные проблемы слушания не внешние, а внутренние — когнитивные и эмоциональные барьеры.",
            "According to Harvard Business Review research, the main listening problems are not external but internal — cognitive and emotional barriers.",
        ),
        "steps": [
            {
                "kind": "lesson",
                "title": ("Ilmiy asos: nega biz eshitmaymiz?", "Ilimiy tiykar: nege biz esitpeymiz?", "Научная основа: почему мы не слышим?", "Scientific basis: why don’t we hear?"),
                "body": (
                    "J. Su va M. Wilkins (2020) to‘rtta ichki to‘siqni ajratadi. 1) Ichki tanqidchi: o‘zingizni doim baholaysiz, diqqat suhbatdoshdan o‘zingizga ko‘chadi. 2) Rolni tor tushunish: o‘zingizni faqat «muammoni hal qiluvchi» deb bilsangiz, tinglash ehtiyoji kamayadi — maslahatchi emas, tushunuvchi hamkor bo‘ling. 3) Oldindan javob tayyorlash: odam gapirayotganda javob o‘ylash ma’noni yo‘qotadi va empatiyani pasaytiradi. 4) Fikrni o‘zgartirishdan qo‘rquv: tinglash o‘rniga o‘z fikrini himoya qilish.\n\n"
                    "R. Nichols va L. Stevens his-tuyg‘ularni «eshitish filtrlari» deb ataydi. Selektiv eshitishda biz faqat o‘z qarashimizga mos gapni qabul qilamiz. Emotsional blokirovkada g‘azab yoki qo‘rquv tinglashni to‘liq to‘sadi — «tanqid», «xato» kabi tetik so‘zlar suhbatni izdan chiqaradi. Tasdiqlovchi og‘ishda esa o‘z fikrimizni tasdiqlovchi ma’lumotni izlab, qarshi fikrlarni inkor qilamiz.\n\n"
                    "Filtrlarni boshqarish uchun: bahoni kechiktiring, faol tinglang, qarama-qarshi fikrlarni ataylab izlang va o‘z reaksiyangizni kuzating.\n\n"
                    "C. Riordan (2020) bo‘yicha empatik tinglash uch qismdan iborat: noverbal signallarni anglash (yuz, ovoz, tana); axborotni chuqur qayta ishlash (asosiy g‘oyani ajratish); reflektiv javob (qayta ifodalash va aniqlashtiruvchi savol). R. Hougaard va J. Carter esa «hozir va shu yerda» bo‘lishni — ichki dialogni susaytirib, butun diqqatni suhbatdoshga qaratishni asosiy shart deb biladi.",
                    "J. Su hám M. Wilkins (2020) tórt ishki tosıqtı ajıratadı. 1) Ishki sınshı: ózińizdi hámme waqıt bahalaysız, dıqqat sáwbetlesiwshiden ózińizge kóshedi. 2) Roldi tar túsiniw: ózińizdi tek «máseleni sheshiwshi» dep bilseńiz, tıńlaw mútájligi azayadı — másláhátshi emes, túsiniwshi sherik bolıń. 3) Aldınnan juwap tayarlaw: adam sóylep atırǵanda juwap oylaw mánisti joǵaltadı hám empatiyanı tómenletedi. 4) Pikirdi ózgertiwden qorqıw: tıńlawdıń ornına óz pikirin qorǵaw.\n\n"
                    "R. Nichols hám L. Stevens sezimlerdi «esitiw filtrleri» dep ataydı. Selektiv esitiwde biz tek óz kózqarasımızǵa say gápti qabıllaymız. Sezimlik blokirovkada ashıw yamasa qorqıw tıńlawdı tolıq jabadı — «sın», «qáte» sıyaqlı qozǵawshı sózler sáwbetti buzadı. Tastıyıqlawshı awıwshılıqta bolsa óz pikirimizdi tastıyıqlaytuǵın maǵlıwmattı izlep, qarsı pikirlerdi biykarlaymız.\n\n"
                    "Filtrlerdi basqarıw ushın: bahalawdı keyinge qaldırıń, belsendi tıńlań, qarama-qarsı pikirlerdi ádeyi izleń hám óz reakciyańızdı baqlań.\n\n"
                    "C. Riordan (2020) boyınsha empatik tıńlaw úsh bólimnen ibarat: noverbal signallardı ańlaw (júz, dawıs, dene); maǵlıwmattı tereń qayta islew (tiykarǵı ideyanı ajıratıw); reflektiv juwap (qayta aytıw hám anıqlawshı soraw). R. Hougaard hám J. Carter bolsa «házir hám usı jerde» bolıwdı — ishki dialogtı páseytip, pútkil dıqqattı sáwbetlesiwshige qaratıwdı tiykarǵı shárt dep biledi.",
                    "Дж. Су и М. Уилкинс (2020) выделяют четыре внутренних барьера. 1) Внутренний критик: вы постоянно оцениваете себя, и внимание уходит от собеседника к себе. 2) Узкое понимание роли: если вы видите себя только «решателем проблем», потребность слушать падает — будьте не советчиком, а понимающим партнёром. 3) Подготовка ответа заранее: обдумывая ответ, пока человек говорит, вы теряете смысл и эмпатию. 4) Страх изменить мнение: вместо слушания — защита своей позиции.\n\n"
                    "Р. Николс и Л. Стивенс называют эмоции «фильтрами слуха». При избирательном слушании мы принимаем только то, что совпадает с нашими взглядами. При эмоциональной блокировке гнев или страх полностью перекрывают слушание — слова-триггеры вроде «критика», «ошибка» срывают разговор. При предвзятости подтверждения мы ищем то, что подтверждает наше мнение, и отвергаем противоположное.\n\n"
                    "Как управлять фильтрами: откладывайте оценку, слушайте активно, намеренно ищите противоположные мнения и наблюдайте за своей реакцией.\n\n"
                    "По К. Риордан (2020), эмпатическое слушание состоит из трёх частей: замечать невербальные сигналы (лицо, голос, тело); глубоко обрабатывать информацию (выделять главную мысль); отвечать рефлексивно (пересказ и уточняющий вопрос). Р. Хугаард и Дж. Картер главным условием считают присутствие «здесь и сейчас» — приглушить внутренний диалог и направить всё внимание на собеседника.",
                    "A. J. Su and M. Wilkins (2020) describe four inner barriers. 1) The inner critic: you keep judging yourself and your attention shifts from the speaker to yourself. 2) A narrow view of your role: if you see yourself only as the “problem solver”, the need to listen drops — be an understanding partner, not an adviser. 3) Preparing your reply: thinking of an answer while the other person speaks loses the meaning and reduces empathy. 4) Fear of changing your mind: defending your view instead of listening.\n\n"
                    "R. Nichols and L. Stevens call emotions “listening filters”. With selective listening we take in only what fits our views. With emotional blocking, anger or fear shuts listening down completely — trigger words like “criticism” or “mistake” derail the conversation. With confirmation bias we look for what confirms our opinion and reject the opposite.\n\n"
                    "To manage the filters: delay judgement, listen actively, deliberately seek opposing views and watch your own reaction.\n\n"
                    "For C. Riordan (2020), empathic listening has three parts: noticing nonverbal signals (face, voice, body); processing information deeply (finding the main idea); responding reflectively (paraphrasing and asking clarifying questions). R. Hougaard and J. Carter see presence — being “here and now”, quieting the inner dialogue and giving the speaker your full attention — as the key condition.",
                ),
            },
            {
                "kind": "quiz",
                "title": ("Test: Men qanday tinglovchiman?", "Test: Men qanday tıńlawshıman?", "Тест: какой я слушатель?", "Test: what kind of listener am I?"),
                "body": TEST_INTRO,
                "results": (
                    (
                        "Tinglashingizga ichki to‘siqlar ko‘p xalaqit beradi. Bir hafta davomida har bir suhbatda faqat bitta qoidaga amal qiling: javob berishdan oldin eshitganingizni bir jumla bilan qayta ayting.",
                        "Tıńlawıńızǵa ishki tosıqlar kóp kesent beredi. Bir hápte dawamında hár bir sáwbette tek bir qaǵıydaǵa ámel etiń: juwap beriwden aldın esitkenińizdi bir gáp penen qayta aytıń.",
                        "Внутренние барьеры сильно мешают вам слушать. Неделю соблюдайте в каждом разговоре одно правило: прежде чем ответить, перескажите услышанное одной фразой.",
                        "Inner barriers get in the way of your listening a lot. For one week follow one rule in every conversation: before replying, repeat what you heard in one sentence.",
                    ),
                    (
                        "Siz yaxshi tinglovchisiz, lekin ba’zan filtrlar ishga tushadi. Qaysi mavzu yoki so‘zlar sizni «yopib qo‘yishini» aniqlang — ular sizning tetiklaringiz.",
                        "Siz jaqsı tıńlawshısız, biraq geyde filtrler iske túsedi. Qaysı tema yamasa sózler sizdi «jabıp qoyatuǵının» anıqlań — olar sizdiń qozǵawshılarıńız.",
                        "Вы хороший слушатель, но иногда включаются фильтры. Определите, какие темы или слова вас «закрывают», — это ваши триггеры.",
                        "You are a good listener, but filters sometimes switch on. Find out which topics or words “shut you down” — those are your triggers.",
                    ),
                    (
                        "Ajoyib! Siz ongli va empatik tinglaysiz. Odamlar siz bilan gaplashganda o‘zlarini tushunilgan his qiladi.",
                        "Ájayıp! Siz sanalı hám empatik tıńlaysız. Adamlar siz benen sóyleskende ózlerin túsinilgen sezedi.",
                        "Отлично! Вы слушаете осознанно и с эмпатией. Рядом с вами люди чувствуют, что их понимают.",
                        "Excellent! You listen mindfully and with empathy. People feel understood when they talk to you.",
                    ),
                ),
                "questions": [
                    (("Odam gapirayotganda men allaqachon javobimni o‘ylayman.", "Adam sóylep atırǵanda men álleqashan juwabımdı oylayman.", "Пока человек говорит, я уже обдумываю свой ответ.", "While someone is talking, I’m already thinking of my reply."), FREQ_R),
                    (("Suhbatda «o‘zimni qanday ko‘rsatyapman» degan o‘y diqqatimni bo‘ladi.", "Sáwbette «ózimdi qalay kórsetip atırman» degen oy dıqqatımdı bóledi.", "В разговоре мысль «как я выгляжу» отвлекает моё внимание.", "In conversation the thought “how do I come across” distracts me."), FREQ_R),
                    (("Fikrimga qarshi gaplarni ham oxirigacha tinglayman.", "Pikirime qarsı gáplerdi de aqırına shekem tıńlayman.", "Я дослушиваю до конца и то, что противоречит моему мнению.", "I listen to the end even when it contradicts my opinion."), FREQ),
                    (("Tushunganimni tekshirish uchun eshitganimni o‘z so‘zlarim bilan qaytaraman.", "Túsingenimdi tekseriw ushın esitkenimdi óz sózlerim menen qaytalayman.", "Чтобы проверить понимание, я пересказываю услышанное своими словами.", "To check I understood, I repeat what I heard in my own words."), FREQ),
                    (("Suhbatdoshim gapirayotganda telefonni chetga qo‘yaman.", "Sáwbetlesiwshim sóylep atırǵanda telefondı shetke qoyaman.", "Когда собеседник говорит, я откладываю телефон.", "When someone is talking to me, I put my phone away."), FREQ),
                ],
            },
            {
                "kind": "scenario",
                "title": ("Amaliy mashq: Tinglash vaziyatlari", "Ámeliy shınıǵıw: Tıńlaw jaǵdayları", "Практика: ситуации слушания", "Practice: listening situations"),
                "body": SCENARIO_INTRO,
                "questions": [
                    (
                        ("Guruhdoshingiz imtihondan yiqilganini va ota-onasidan qo‘rqayotganini aytyapti.", "Toparlasıńız imtixannan ótpegenin hám ata-anasınan qorqıp atırǵanın aytıp atır.", "Одногруппник рассказывает, что провалил экзамен и боится реакции родителей.", "A groupmate tells you they failed an exam and are afraid of their parents’ reaction."),
                        (
                            "«Hech gap emas, qayta topshirasan» deb darhol maslahat beraman | 1 | Niyat yaxshi, lekin shoshilinch maslahat — «muammoni hal qiluvchi» rolining tor talqini. Avval tinglang.\n«Qo‘rqayotganingni tushunaman. Nima bo‘ldi, aytib ber» deyman | 2 | To‘g‘ri! Reflektiv javob va ochiq savol — empatik tinglashning asosi.\n«Men ham yiqilganman, mana bunday bo‘lgan edi...» deb o‘z hikoyamni aytaman | 0 | Diqqat o‘zingizga ko‘chdi — suhbatdosh eshitilmay qoldi.",
                            "«Túk etpeydi, qayta tapsırasań» dep dárhal másláhát beremen | 1 | Niyet jaqsı, biraq asıǵıs másláhát — «máseleni sheshiwshi» roliniń tar túsinigi. Aldın tıńlań.\n«Qorqıp atırǵanıńdı túsinemen. Ne boldı, aytıp ber» deymen | 2 | Durıs! Reflektiv juwap hám ashıq soraw — empatik tıńlawdıń tiykarı.\n«Men de ótpegenmen, mine bılay bolǵan edi...» dep óz gúrrińimdi aytaman | 0 | Dıqqat ózińizge kóshti — sáwbetlesiwshi esitilmey qaldı.",
                            "Сразу посоветую: «Ерунда, пересдашь» | 1 | Намерение доброе, но поспешный совет — узкое понимание роли «решателя». Сначала выслушайте.\nСкажу: «Понимаю, что тебе страшно. Расскажи, что случилось» | 2 | Верно! Рефлексивный ответ и открытый вопрос — основа эмпатического слушания.\nРасскажу свою историю: «Я тоже заваливал, было так…» | 0 | Внимание ушло к вам — собеседника не услышали.",
                            "Immediately advise: “No big deal, you’ll retake it” | 1 | Good intention, but quick advice is the narrow “problem solver” role. Listen first.\nSay: “I understand you’re scared. Tell me what happened” | 2 | Right! A reflective response and an open question are the core of empathic listening.\nTell my own story: “I failed once too, here’s what happened…” | 0 | The attention moved to you — the speaker wasn’t heard.",
                        ),
                    ),
                    (
                        ("O‘qituvchi ishingizni tanqid qilyapti. Ichingizda g‘azab ko‘tarilyapti.", "Oqıtıwshı jumısıńızdı sınǵa alıp atır. Ishińizde ashıw kóterilip atır.", "Преподаватель критикует вашу работу. Внутри поднимается гнев.", "A teacher is criticising your work. Anger is rising inside you."),
                        (
                            "Darhol e’tiroz bildirib, o‘zimni oqlay boshlayman | 0 | Emotsional blokirovka: g‘azab filtri tinglashni yopdi, foydali fikrlar eshitilmay qoldi.\nNafas olib, bahoni kechiktiraman va «Qaysi joyini yaxshilashim kerak?» deb so‘rayman | 2 | Ajoyib! Siz filtrni sezib, bahoni kechiktirdingiz va aniqlashtiruvchi savol berdingiz.\nIndamay o‘tiraman, lekin ichimda «u meni yomon ko‘radi» deb o‘ylayman | 1 | Tashqi tomondan tinch, lekin tasdiqlovchi og‘ish ishlayapti — siz faqat o‘z taxminingizni eshityapsiz.",
                            "Dárhal qarsılıq bildirip, ózimdi aqlay baslayman | 0 | Sezimlik blokirovka: ashıw filtri tıńlawdı japtı, paydalı pikirler esitilmey qaldı.\nDem alıp, bahalawdı keyinge qaldıraman hám «Qay jerin jaqsılawım kerek?» dep sorayman | 2 | Ájayıp! Siz filtrdi sezip, bahalawdı keyinge qaldırdıńız hám anıqlawshı soraw berdińiz.\nÚndemey otıraman, biraq ishimde «ol meni jaqtırmaydı» dep oylayman | 1 | Sırttan tınısh, biraq tastıyıqlawshı awıwshılıq islep atır — siz tek óz boljawıńızdı esitip atırsız.",
                            "Сразу начну возражать и оправдываться | 0 | Эмоциональная блокировка: фильтр гнева закрыл слушание, полезное не услышано.\nСделаю вдох, отложу оценку и спрошу: «Что именно мне улучшить?» | 2 | Отлично! Вы заметили фильтр, отложили оценку и задали уточняющий вопрос.\nПромолчу, но про себя подумаю: «Он меня не любит» | 1 | Внешне спокойно, но работает предвзятость подтверждения — вы слышите только своё предположение.",
                            "Immediately object and start justifying myself | 0 | Emotional blocking: the anger filter shut listening down and the useful points were lost.\nTake a breath, delay judgement and ask: “What exactly should I improve?” | 2 | Excellent! You noticed the filter, delayed judgement and asked a clarifying question.\nStay silent but think “they don’t like me” | 1 | Calm on the outside, but confirmation bias is at work — you only hear your own assumption.",
                        ),
                    ),
                    (
                        ("Do‘stingiz uzoq gapiryapti, telefoningizga xabar keldi.", "Dostıńız uzaq sóylep atır, telefonıńızǵa xabar keldi.", "Друг долго рассказывает, а вам пришло сообщение.", "Your friend is talking at length and a message arrives on your phone."),
                        (
                            "«Bir soniya» deb xabarni o‘qiyman va keyin davom ettiramiz | 1 | Ochiq aytganingiz yaxshi, lekin diqqatning bo‘linishi muloqot sifatini pasaytiradi.\nTelefonni teskari qo‘yib, unga qarab tinglashda davom etaman | 2 | To‘g‘ri! Bu — ongli ishtirok: «hozir va shu yerda» bo‘lish ishonchni oshiradi.\nBosh irg‘ab turib, yashirincha xabarni o‘qiyman | 0 | Odamlar bo‘lingan diqqatni sezadi — bu ishonchni susaytiradi.",
                            "«Bir minut» dep xabardı oqıyman hám keyin dawam etemiz | 1 | Ashıq aytqanıńız jaqsı, biraq dıqqattıń bóliniwi qarım-qatnas sapasın tómenletedi.\nTelefondı tóńkerip qoyıp, oǵan qarap tıńlawdı dawam etemen | 2 | Durıs! Bul — sanalı qatnasıw: «házir hám usı jerde» bolıw isenimdi arttıradı.\nBas iyzep turıp, jasırın xabardı oqıyman | 0 | Adamlar bólingen dıqqattı sezedi — bul isenimdi álsiretedi.",
                            "Скажу «секунду», прочитаю сообщение и продолжим | 1 | Хорошо, что сказали прямо, но рассеянное внимание снижает качество общения.\nПереверну телефон экраном вниз и продолжу слушать, глядя на друга | 2 | Верно! Это осознанное присутствие: быть «здесь и сейчас» — значит укреплять доверие.\nБуду кивать и украдкой читать сообщение | 0 | Люди замечают рассеянное внимание — это подрывает доверие.",
                            "Say “one second”, read the message and then continue | 1 | Good that you said so, but divided attention lowers the quality of the conversation.\nTurn the phone face down and keep listening, looking at my friend | 2 | Right! This is presence: being “here and now” builds trust.\nKeep nodding and secretly read the message | 0 | People notice divided attention — it erodes trust.",
                        ),
                    ),
                ],
            },
            {
                "kind": "reflection",
                "title": ("O‘zingizga yordam: mening asosiy to‘sig‘im", "Ózińizge járdem: meniń tiykarǵı tosıǵım", "Помоги себе: мой главный барьер", "Self-help: my main barrier"),
                "body": (
                    "To‘rt ichki to‘siq va uch filtrdan qaysi biri sizga ko‘proq xalaqit beradi? Uni keyingi muhim suhbatda qanday kuzatib, to‘xtatasiz — aniq bir qadamni yozing.",
                    "Tórt ishki tosıq hám úsh filtrden qaysısı sizge kóbirek kesent beredi? Onı keyingi áhmiyetli sáwbette qalay baqlap, toqtatasız — anıq bir qádemdi jazıń.",
                    "Какой из четырёх барьеров и трёх фильтров мешает вам больше всего? Как вы заметите и остановите его в следующем важном разговоре — запишите один конкретный шаг.",
                    "Which of the four barriers and three filters gets in your way most? Write one concrete step for how you’ll notice and stop it in your next important conversation.",
                ),
            },
        ],
    },
    # ------------------------------------------------------------------ 7
    {
        "slug": "ei-7-relationships-and-conflict",
        "order": 7,
        "icon": "🕊️",
        "color": "rose",
        "level": "intermediate",
        "minutes": 20,
        "tags": "relationships, conflict, communication, humor",
        "sources": (
            "Bradberry T., Greaves J. Emotional Intelligence 2.0. – San Diego: TalentSmart, 2009.\n"
            "Lemberg B. Emotsional intellekt: aql va his-tuyg‘ular o‘rtasidagi muloqot. – 2013.\n"
            "Goleman D. Emotional Intelligence: Why It Can Matter More Than IQ. – New York: Bantam Books, 1995.\n"
            "Martin R. A. et al. Individual differences in uses of humor and their relation to psychological well-being // Journal of Research in Personality. – 2003. – Vol. 37(1). – P. 48–75."
        ),
        "title": ("Munosabatlar va nizolarni hal qilish", "Qatnaslar hám kelispewshiliklerdi sheshiw", "Отношения и разрешение конфликтов", "Relationships and resolving conflict"),
        "summary": (
            "Munosabatlarni boshqarish, nizolarni konstruktiv hal etish qoidalari va hazilning sog‘lom turlari.",
            "Qatnaslardı basqarıw, kelispewshiliklerdi konstruktiv sheshiw qaǵıydaları hám hazildiń salamat túrleri.",
            "Управление отношениями, правила конструктивного решения конфликтов и здоровые виды юмора.",
            "Managing relationships, rules for constructive conflict resolution and healthy kinds of humour.",
        ),
        "goal": (
            "Nizoni janjalga emas, munosabatni mustahkamlashga aylantiradigan to‘rt qoidani amalda qo‘llashni o‘rganasiz.",
            "Kelispewshilikti janjelge emes, qatnastı bekkemlewge aylandıratuǵın tórt qaǵıydanı ámelde qollanıwdı úyrenesiz.",
            "Вы научитесь применять четыре правила, которые превращают конфликт не в ссору, а в укрепление отношений.",
            "You will learn to use four rules that turn a conflict into a stronger relationship rather than a fight.",
        ),
        "description": description(
            "Munosabatlarni boshqarish — hissiy intellektning eng murakkab ko‘nikmasi. U oldingi uchtasiga tayanadi: o‘zini anglamagan va boshqara olmagan odam boshqalar bilan yaxshi munosabat qura olmaydi.",
            "Qatnaslardı basqarıw — emocional intellekttiń eń quramalı kónlikpesi. Ol aldıńǵı úshewine súyenedi: ózin ańlamaǵan hám basqara almaǵan adam basqalar menen jaqsı qatnas qura almaydı.",
            "Управление отношениями — самый сложный навык эмоционального интеллекта. Он опирается на три предыдущих: кто не осознаёт себя и не управляет собой, не построит хороших отношений.",
            "Relationship management is the most complex emotional intelligence skill. It rests on the previous three: someone who isn’t self-aware and can’t manage themselves can’t build good relationships.",
        ),
        "steps": [
            {
                "kind": "lesson",
                "title": ("Ilmiy asos: nizo — o‘sish imkoniyati", "Ilimiy tiykar: kelispewshilik — ósiw múmkinshiligi", "Научная основа: конфликт — возможность роста", "Scientific basis: conflict is a chance to grow"),
                "body": (
                    "Bradberry va Greaves (2009) bo‘yicha munosabatlarni boshqarish samarali muloqot, nizolarni boshqarish, jamoada ishlash va ijobiy ta’sir ko‘rsatishni qamrab oladi. Bu daraja oldingi uch ko‘nikmasiz shakllanmaydi.\n\n"
                    "Nizolar munosabatlarning tabiiy qismi. B. Lemberg (2013) nizolarni konstruktiv hal etish uchun to‘rt qoidani beradi: 1) o‘tmishni emas, hozirgi vaziyatni muhokama qiling; 2) muhim va nomuhim masalalarni ajrating — har bir bahsda g‘alaba shart emas; 3) kechira oling; 4) yechimi yo‘q bahsni to‘xtating — «bu borada fikrimiz har xil» deyish ham yechim.\n\n"
                    "Hazil va o‘yin stressga qarshi tabiiy vosita: ular kayfiyatni ko‘taradi, muammoga yangi nuqtai nazardan qarashga yordam beradi. Tadqiqotlar ko‘rsatadiki, hissiy intellekt yuqori odamlar birlashtiruvchi va o‘zini qo‘llab-quvvatlovchi hazildan, past bo‘lganlar esa tajovuzkor va o‘zini kamsituvchi hazildan ko‘proq foydalanadi.\n\n"
                    "Agar nizo to‘g‘ri boshqarilsa, u ishonch va hamkorlikni mustahkamlovchi vositaga aylanadi. Asosiy formula: avval o‘zingizni tinchlantiring, keyin tinglang, keyin o‘z ehtiyojingizni «men» shaklida ayting: «Kechikkaningda men xavotirlanaman».",
                    "Bradberry hám Greaves (2009) boyınsha qatnaslardı basqarıw nátiyjeli qarım-qatnas, kelispewshiliklerdi basqarıw, toparda islew hám unamlı tásir kórsetiwdi qamtıydı. Bul dáreje aldıńǵı úsh kónlikpesiz qáliplespeydi.\n\n"
                    "Kelispewshilikler qatnaslardıń tábiyiy bólegi. B. Lemberg (2013) kelispewshiliklerdi konstruktiv sheshiw ushın tórt qaǵıydanı beredi: 1) ótmishti emes, házirgi jaǵdaydı talqılań; 2) áhmiyetli hám áhmiyetsiz máselelerdi ajıratıń — hár bir tartısta jeńis shárt emes; 3) keshire alıń; 4) sheshimi joq tartıstı toqtatıń — «bul boyınsha pikirimiz hár qıylı» dew de sheshim.\n\n"
                    "Hazil hám oyın stresske qarsı tábiyiy qural: olar kewil-kúydi kóteredi, máselege jańa kózqarastan qarawǵa járdem beredi. Izertlewler kórsetkenindey, emocional intellekti joqarı adamlar biriktiriwshi hám ózin qollap-quwatlawshı hazilden, tómen bolǵanlar bolsa tajawızkor hám ózin kemsitiwshi hazilden kóbirek paydalanadı.\n\n"
                    "Eger kelispewshilik durıs basqarılsa, ol isenim hám birge islesiwdi bekkemlewshi qoralǵa aylanadı. Tiykarǵı formula: aldın ózińizdi tınıshlandırıń, keyin tıńlań, keyin óz mútájligińizdi «men» formasında aytıń: «Keshikkenińde men tınıshsızlanaman».",
                    "По Брэдбери и Гривз (2009), управление отношениями включает эффективное общение, управление конфликтами, работу в команде и позитивное влияние. Этот уровень не формируется без трёх предыдущих навыков.\n\n"
                    "Конфликты — естественная часть отношений. Б. Лемберг (2013) даёт четыре правила конструктивного решения: 1) обсуждайте нынешнюю ситуацию, а не прошлое; 2) отделяйте важное от неважного — не в каждом споре нужна победа; 3) умейте прощать; 4) прекращайте спор, у которого нет решения, — «у нас разные мнения» тоже решение.\n\n"
                    "Юмор и игра — естественное средство против стресса: поднимают настроение и помогают взглянуть на проблему по-новому. Исследования показывают: люди с высоким эмоциональным интеллектом чаще используют объединяющий и поддерживающий себя юмор, с низким — агрессивный и самоуничижительный.\n\n"
                    "Если конфликт управляется правильно, он укрепляет доверие и сотрудничество. Главная формула: сначала успокойтесь, потом выслушайте, потом скажите о своей потребности в форме «я»: «Когда ты опаздываешь, я волнуюсь».",
                    "For Bradberry and Greaves (2009), relationship management covers effective communication, managing conflict, teamwork and positive influence. It doesn’t develop without the previous three skills.\n\n"
                    "Conflicts are a natural part of relationships. B. Lemberg (2013) gives four rules for constructive resolution: 1) discuss the present situation, not the past; 2) separate what matters from what doesn’t — you don’t need to win every argument; 3) be able to forgive; 4) stop arguments that have no solution — “we see this differently” is also a solution.\n\n"
                    "Humour and play are natural antidotes to stress: they lift the mood and help you see a problem from a new angle. Research shows people with high emotional intelligence use more affiliative and self-supporting humour, while people with low emotional intelligence use more aggressive and self-defeating humour.\n\n"
                    "Handled well, conflict strengthens trust and cooperation. The core formula: calm yourself first, then listen, then state your need as an “I” message: “When you’re late, I get worried.”",
                ),
            },
            {
                "kind": "quiz",
                "title": ("Test: Nizolarda o‘zimni qanday tutaman?", "Test: Kelispewshiliklerde ózimdi qalay tutaman?", "Тест: как я веду себя в конфликтах?", "Test: how do I behave in conflicts?"),
                "body": TEST_INTRO,
                "results": (
                    (
                        "Nizolar siz uchun og‘ir kechadi va ko‘pincha janjalga aylanadi. Keyingi bahsda faqat bitta qoidani sinab ko‘ring: o‘tmishni eslatmasdan, faqat hozirgi masala haqida gapiring.",
                        "Kelispewshilikler siz ushın awır ótedi hám kóbinese janjelge aylanadı. Keyingi tartısta tek bir qaǵıydanı sınap kóriń: ótmishti eslatpay, tek házirgi másele haqqında sóyleń.",
                        "Конфликты даются вам тяжело и часто перерастают в ссоры. В следующем споре попробуйте одно правило: говорите только о нынешнем вопросе, не вспоминая прошлое.",
                        "Conflicts are hard for you and often turn into fights. In your next argument try one rule: talk only about the current issue, without bringing up the past.",
                    ),
                    (
                        "Siz ko‘pincha nizolarni tinch hal qilasiz. «Men» shaklidagi gaplarni ko‘proq ishlating va yechimi yo‘q bahslarni vaqtida to‘xtatishni o‘rganing.",
                        "Siz kóbinese kelispewshiliklerdi tınısh sheshesiz. «Men» formasındaǵı gáplerdi kóbirek qollanıń hám sheshimi joq tartıslardı óz waqtında toqtatıwdı úyreniń.",
                        "Чаще всего вы решаете конфликты мирно. Чаще используйте «я-высказывания» и учитесь вовремя останавливать споры без решения.",
                        "You usually resolve conflicts peacefully. Use more “I” messages and learn to stop unsolvable arguments in time.",
                    ),
                    (
                        "Ajoyib! Siz nizolarni munosabatni mustahkamlash imkoniyatiga aylantira olasiz. Bu ko‘nikmangiz bilan guruhda vositachi bo‘la olasiz.",
                        "Ájayıp! Siz kelispewshiliklerdi qatnastı bekkemlew múmkinshiligine aylandıra alasız. Bul kónlikpeńiz benen toparda dánekershi bola alasız.",
                        "Отлично! Вы умеете превращать конфликт в возможность укрепить отношения. С таким навыком вы можете быть посредником в группе.",
                        "Excellent! You can turn conflict into a chance to strengthen relationships. With this skill you can be a mediator in your group.",
                    ),
                ),
                "questions": [
                    (("Bahs paytida o‘tmishdagi xatolarni eslatib qo‘yaman.", "Tartıs waqtında ótmishtegi qátelerdi eslatıp qoyaman.", "Во время спора я припоминаю прошлые ошибки.", "During arguments I bring up past mistakes."), FREQ_R),
                    (("Arzimas narsa uchun bahsda g‘alaba qozonishga intilaman.", "Arzımas nárse ushın tartısta jeńiske umtılaman.", "Я стремлюсь победить в споре даже из-за мелочи.", "I try to win arguments even over small things."), FREQ_R),
                    (("Xafa qilgan odamni kechira olaman.", "Renjitken adamdı keshire alaman.", "Я могу простить человека, который меня обидел.", "I can forgive someone who hurt me."), FREQ),
                    (("Nizoli paytda ham his-tuyg‘ularimni «men» shaklida aytaman.", "Kelispewshilik waqtında da sezimlerimdi «men» formasında aytaman.", "Даже в конфликте я говорю о чувствах в форме «я».", "Even in conflict I express my feelings with “I” statements."), FREQ),
                    (("Keskin vaziyatni yengillashtirish uchun mehribon hazildan foydalanaman.", "Keskin jaǵdaydı jeńillestiriw ushın meyirli hazilden paydalanaman.", "Чтобы разрядить напряжение, я использую добрый юмор.", "I use kind humour to ease a tense situation."), FREQ),
                ],
            },
            {
                "kind": "scenario",
                "title": ("Amaliy mashq: Nizoni hal qilamiz", "Ámeliy shınıǵıw: Kelispewshilikti sheshemiz", "Практика: решаем конфликт", "Practice: resolving a conflict"),
                "body": SCENARIO_INTRO,
                "questions": [
                    (
                        ("Xonadoshingiz yana idishlarni yuvmay qoldirdi. Bu uchinchi marta.", "Bólmeles dostıńız jáne ıdıslardı juwmay qaldırdı. Bul úshinshi ret.", "Сосед по комнате снова не помыл посуду. Это уже третий раз.", "Your roommate left the dishes unwashed again. It’s the third time."),
                        (
                            "«Sen doim shunaqasan, o‘tgan oy ham...» deb boshlayman | 0 | «Doim» va o‘tmishni eslatish odamni himoyaga o‘tkazadi — nizo kuchayadi.\n«Idishlar qolganda men charchayman. Navbat jadvali tuzamizmi?» deyman | 2 | To‘g‘ri! Hozirgi masala, «men» shaklidagi gap va birgalikdagi yechim.\nIndamay o‘zim yuvaman, lekin ichimda xafa bo‘lib yuraman | 1 | Tinchlik saqlandi, lekin to‘plangan xafagarchilik keyin portlashi mumkin.",
                            "«Sen hámme waqıt usındaysań, ótken ay da...» dep baslayman | 0 | «Hámme waqıt» hám ótmishti eslatıw adamdı qorǵanıwǵa ótkeredi — kelispewshilik kúsheyedi.\n«Ídıslar qalǵanda men sharshayman. Gezek kestesin dúzemiz be?» deymen | 2 | Durıs! Házirgi másele, «men» formasındaǵı gáp hám birgeliktegi sheshim.\nÚndemey ózim juwaman, biraq ishimde renjip júremen | 1 | Tınıshlıq saqlandı, biraq jıynalǵan renjiw keyin jarılıwı múmkin.",
                            "Начну с «Ты всегда такой, и в прошлом месяце…» | 0 | «Всегда» и упрёки прошлым заставляют защищаться — конфликт растёт.\nСкажу: «Когда посуда остаётся, я устаю. Давай составим график?» | 2 | Верно! Нынешний вопрос, «я-высказывание» и совместное решение.\nМолча помою сам, но буду носить обиду | 1 | Мир сохранён, но накопленная обида может потом взорваться.",
                            "Start with “You always do this, last month too…” | 0 | “Always” and past blame make people defensive — the conflict grows.\nSay: “When dishes are left, I get tired. Shall we make a rota?” | 2 | Right! The current issue, an “I” message and a shared solution.\nWash them myself in silence but stay resentful | 1 | Peace is kept, but built-up resentment can explode later.",
                        ),
                    ),
                    (
                        ("Do‘stingiz bilan qaysi film yaxshiroq ekani haqida bahs qizib ketdi.", "Dostıńız benen qaysı film jaqsıraq ekeni haqqında tartıs qızıp ketti.", "Спор с другом о том, какой фильм лучше, накалился.", "An argument with your friend about which film is better is heating up."),
                        (
                            "U tan olguncha dalillar keltiraveraman | 0 | Bu nomuhim masala — g‘alaba do‘stlikdan qimmat emas.\nKulib, «Mayli, didlarimiz har xil — bu ham yaxshi» deyman | 2 | Ajoyib! Muhimni nomuhimdan ajratdingiz va mehribon hazil bilan yechimi yo‘q bahsni to‘xtatdingiz.\n«Sening diding yo‘q» deb hazillashaman | 1 | Hazil — lekin tajovuzkor. Bunday hazil munosabatga zarar yetkazadi.",
                            "Ol moyınlaǵansha dálil keltire beremen | 0 | Bul áhmiyetsiz másele — jeńis doslıqtan qımbat emes.\nKúlip, «Meyli, talǵamlarımız hár qıylı — bul da jaqsı» deymen | 2 | Ájayıp! Áhmiyetlini áhmiyetsizden ajırattıńız hám meyirli hazil menen sheshimi joq tartıstı toqtattıńız.\n«Seniń talǵamıń joq» dep hazillesemen | 1 | Hazil — biraq tajawızkor. Bunday hazil qatnasqa ziyan keltiredi.",
                            "Буду приводить аргументы, пока он не признает | 0 | Это неважный вопрос — победа не дороже дружбы.\nЗасмеюсь: «Ладно, вкусы у нас разные — и это нормально» | 2 | Отлично! Вы отделили важное от неважного и добрым юмором остановили спор без решения.\nПошучу: «У тебя просто нет вкуса» | 1 | Юмор — но агрессивный. Такие шутки вредят отношениям.",
                            "Keep giving arguments until they admit I’m right | 0 | This doesn’t matter — winning isn’t worth more than the friendship.\nLaugh: “OK, our tastes differ — and that’s fine” | 2 | Excellent! You separated the important from the trivial and ended an unsolvable argument with kind humour.\nJoke: “You just have no taste” | 1 | Humour — but aggressive. Jokes like this hurt relationships.",
                        ),
                    ),
                    (
                        ("Opa-singlingiz kecha sizni xafa qildi va bugun kechirim so‘radi.", "Apa-sińlińiz keshe sizdi renjitti hám búgin keshirim soradı.", "Сестра вчера вас обидела, а сегодня попросила прощения.", "Your sister hurt you yesterday and apologised today."),
                        (
                            "Kechiraman va nimani his qilganimni xotirjam aytaman | 2 | To‘g‘ri! Kechira olish va his-tuyg‘uni ochiq aytish munosabatni tiklaydi.\n«Mayli» deyman, lekin bir hafta gaplashmayman | 0 | So‘zda kechirim, amalda jazo — bu ishonchni yemiradi.\nKechiraman, lekin keyingi bahsda buni albatta eslataman | 1 | Kechirim chala qoldi: o‘tmishni qurol qilish nizolarni kuchaytiradi.",
                            "Keshiremen hám neni sezgenimdi tınısh aytaman | 2 | Durıs! Keshire alıw hám sezimdi ashıq aytıw qatnastı tikleydi.\n«Meyli» deymen, biraq bir hápte sóylespeymen | 0 | Sózde keshirim, ámelde jaza — bul isenimdi buzadı.\nKeshiremen, biraq keyingi tartısta bunı álbette eslataman | 1 | Keshirim shala qaldı: ótmishti qural etiw kelispewshiliklerdi kúsheytedi.",
                            "Прощу и спокойно скажу, что почувствовал | 2 | Верно! Умение прощать и открыто говорить о чувствах восстанавливает отношения.\nСкажу «ладно», но неделю не буду разговаривать | 0 | Прощение на словах, наказание на деле — это разрушает доверие.\nПрощу, но в следующем споре обязательно припомню | 1 | Прощение неполное: прошлое как оружие усиливает конфликты.",
                            "Forgive her and calmly say how I felt | 2 | Right! Forgiving and openly naming feelings repairs the relationship.\nSay “fine” but not speak to her for a week | 0 | Forgiveness in words, punishment in deeds — this destroys trust.\nForgive her but definitely bring it up in the next argument | 1 | Incomplete forgiveness: using the past as a weapon fuels conflict.",
                        ),
                    ),
                ],
            },
            {
                "kind": "reflection",
                "title": ("O‘zingizga yordam: «men» tilida gapiramiz", "Ózińizge járdem: «men» tilinde sóyleymiz", "Помоги себе: говорим на языке «я»", "Self-help: speaking in “I” messages"),
                "body": (
                    "Hozir hal bo‘lmagan bitta kelishmovchilikni eslang. Uni «Qachonki ..., men ... his qilaman, chunki menga ... muhim. Keling, ...» shaklida yozib ko‘ring.",
                    "Házir sheshilmegen bir kelispewshilikti eslań. Onı «Qashan ..., men ... sezemen, sebebi maǵan ... áhmiyetli. Keliń, ...» formasında jazıp kóriń.",
                    "Вспомните одно нерешённое разногласие. Сформулируйте его так: «Когда ..., я чувствую ..., потому что мне важно ... Давай ...».",
                    "Recall one unresolved disagreement. Write it as: “When ..., I feel ..., because ... matters to me. Let’s ...”.",
                ),
            },
        ],
    },
    # ------------------------------------------------------------------ 8
    {
        "slug": "ei-8-emotional-literacy",
        "order": 8,
        "icon": "💗",
        "color": "rose",
        "level": "advanced",
        "minutes": 20,
        "tags": "emotional literacy, empathy, relationships, self-knowledge",
        "sources": (
            "Steiner C. M. Emotional Literacy: Intelligence with a Heart. – California: Personhood Press, 2003.\n"
            "Goleman D. Emotional Intelligence: Why It Can Matter More Than IQ. – New York: Bantam Books, 1995.\n"
            "Salovey P., Mayer J. D. Emotional intelligence // Imagination, Cognition and Personality. – 1990. – Vol. 9(3). – P. 185–211."
        ),
        "title": ("Emotsional savodxonlik: yurak bilan intellekt", "Emocional sawatlılıq: júrek penen intellekt", "Эмоциональная грамотность: интеллект с сердцем", "Emotional literacy: intelligence with a heart"),
        "summary": (
            "Claude Steinerning besh ko‘nikmasi: o‘zini anglash, empatiya, boshqarish, javobgarlik va kechirim so‘rash.",
            "Claude Steinerdiń bes kónlikpesi: ózin ańlaw, empatiya, basqarıw, juwapkershilik hám keshirim soraw.",
            "Пять навыков Клода Штайнера: самоосознание, эмпатия, управление, ответственность и умение извиняться.",
            "Claude Steiner’s five skills: self-awareness, empathy, management, responsibility and apologising.",
        ),
        "goal": (
            "His-tuyg‘ularingizni ochiq va hurmat bilan ifodalash, xatoingiz uchun chin dildan kechirim so‘rashni o‘rganasiz — o‘zingizga va yaqinlaringizga yordam berish ko‘nikmasi.",
            "Sezimlerińizdi ashıq hám húrmet penen bildiriw, qátelerińiz ushın shın kewilden keshirim sorawdı úyrenesiz — ózińizge hám jaqınlarıńızǵa járdem beriw kónlikpesi.",
            "Вы научитесь открыто и уважительно выражать чувства и искренне извиняться за ошибки — это навык помогать себе и близким.",
            "You will learn to express feelings openly and respectfully and to apologise sincerely — a skill for helping yourself and the people close to you.",
        ),
        "description": description(
            "Kursning yakuniy mavzusi. Steiner bo‘yicha emotsional savodxonlik — «yurakka yo‘naltirilgan hissiy intellekt»: his-tuyg‘ularni odamlarni birlashtiradigan kuchga aylantirish.",
            "Kurstıń juwmaqlawshı teması. Steiner boyınsha emocional sawatlılıq — «júrekke baǵdarlanǵan emocional intellekt»: sezimlerdi adamlardı biriktiretuǵın kúshke aylandırıw.",
            "Заключительная тема курса. По Штайнеру, эмоциональная грамотность — «эмоциональный интеллект, направленный сердцем»: превращение чувств в силу, которая объединяет людей.",
            "The final topic of the course. For Steiner, emotional literacy is “emotional intelligence with a heart”: turning feelings into a force that brings people together.",
        ),
        "steps": [
            {
                "kind": "lesson",
                "title": ("Ilmiy asos: Steinerning besh ko‘nikmasi", "Ilimiy tiykar: Steinerdiń bes kónlikpesi", "Научная основа: пять навыков Штайнера", "Scientific basis: Steiner’s five skills"),
                "body": (
                    "«Hissiy intellekt» atamasini Salovey va Mayer kiritgan bo‘lsa, «emotsional savodxonlik»ni amerikalik psixolog Claude Steiner (2003) ilgari surgan. Uning ta’rificha, bu — muhabbatga yo‘naltirilgan hissiy intellekt. Bu yerda muhabbat faqat romantik tuyg‘u emas: o‘zini qabul qilish, boshqalarga ijobiy munosabat, yaqinlik va ishonch.\n\n"
                    "Steiner besh ko‘nikmani ajratadi: 1) o‘z his-tuyg‘ularini, ularning sababi va kuchini anglash; 2) empatik sezgirlik — «emotsional rezonans»; 3) his-tuyg‘ularni boshqarish — ijobiylarini mustahkamlash, salbiylarini konstruktiv ifodalash; 4) yetkazilgan emotsional zarar uchun javobgarlik — kechirim so‘rash va vaziyatni tiklash; 5) emotsional interaktivlik — barcha ko‘nikmalarni murakkab vaziyatda birga qo‘llash.\n\n"
                    "Steiner fikricha, bolalikdagi tajribalar tufayli ko‘p odamlarda his-tuyg‘ularni erkin ifodalash qobiliyati susaygan, ammo uni tranzaksion tahlil mashqlari orqali qayta tiklash mumkin. His-tuyg‘ularni bostirish ularni yo‘q qilmaydi — psixologik muammolarga olib keladi.\n\n"
                    "Emotsional savodxonlik shaxsiy kuchni oshiradi, munosabatlarni yaxshilaydi va ijtimoiy moslashuvni rivojlantiradi. Goleman (1995) xulosasi: his-tuyg‘ularni boshqarish — ularni bostirish emas, balki anglash va ongli ravishda yo‘naltirish. Bu kursning barcha mavzulari aynan shu natijaga — o‘zingizga psixologik yordam bera olishga olib keladi.",
                    "«Emocional intellekt» terminin Salovey hám Mayer kirgizgen bolsa, «emocional sawatlılıqtı» amerikalı psixolog Claude Steiner (2003) usınǵan. Onıń anıqlamasınsha, bul — súyispenshilikke baǵdarlanǵan emocional intellekt. Bul jerde súyispenshilik tek romantik sezim emes: ózin qabıllaw, basqalarǵa unamlı qatnas, jaqınlıq hám isenim.\n\n"
                    "Steiner bes kónlikpeni ajıratadı: 1) óz sezimlerin, olardıń sebebin hám kúshin ańlaw; 2) empatik sezgirlik — «sezimlik rezonans»; 3) sezimlerdi basqarıw — unamlıların bekkemlew, unamsızların konstruktiv bildiriw; 4) jetkerilgen sezimlik ziyan ushın juwapkershilik — keshirim soraw hám jaǵdaydı tiklew; 5) sezimlik interaktivlik — barlıq kónlikpelerdi quramalı jaǵdayda birge qollanıw.\n\n"
                    "Steiner pikirinshe, balalıqtaǵı tájiriybeler sebepli kóp adamlarda sezimlerdi erkin bildiriw qábileti álsiregen, biraq onı tranzakciyalıq analiz shınıǵıwları arqalı qayta tiklewge boladı. Sezimlerdi basıw olardı joq etpeydi — psixologiyalıq máselelerge alıp keledi.\n\n"
                    "Emocional sawatlılıq jeke kúshti arttıradı, qatnaslardı jaqsılaydı hám social beyimlesiwdi rawajlandıradı. Goleman (1995) juwmaǵı: sezimlerdi basqarıw — olardı basıw emes, al ańlaw hám sanalı túrde baǵdarlaw. Bul kurstıń barlıq temaları usı nátiyjege — ózińizge psixologiyalıq járdem bere alıwǵa alıp keledi.",
                    "Если термин «эмоциональный интеллект» ввели Сэловей и Майер, то «эмоциональную грамотность» предложил американский психолог Клод Штайнер (2003). По его определению, это эмоциональный интеллект, направленный любовью. Любовь здесь не только романтическое чувство: это принятие себя, доброжелательность к другим, близость и доверие.\n\n"
                    "Штайнер выделяет пять навыков: 1) осознавать свои чувства, их причину и силу; 2) эмпатическая чуткость — «эмоциональный резонанс»; 3) управлять эмоциями — укреплять позитивные, конструктивно выражать негативные; 4) ответственность за причинённый эмоциональный вред — извиниться и исправить ситуацию; 5) эмоциональная интерактивность — применять все навыки вместе в сложной ситуации.\n\n"
                    "По Штайнеру, из-за детского опыта у многих ослабла способность свободно выражать чувства, но её можно восстановить упражнениями транзактного анализа. Подавление чувств их не уничтожает — оно ведёт к психологическим проблемам.\n\n"
                    "Эмоциональная грамотность усиливает личную силу, улучшает отношения и развивает социальную адаптацию. Вывод Гоулмана (1995): управлять эмоциями — значит не подавлять их, а осознавать и сознательно направлять. Все темы курса ведут именно к этому результату — умению оказать психологическую помощь самому себе.",
                    "While “emotional intelligence” was coined by Salovey and Mayer, “emotional literacy” was proposed by the American psychologist Claude Steiner (2003). He defines it as emotional intelligence centred on love. Love here is not only romance: it means accepting yourself, goodwill towards others, closeness and trust.\n\n"
                    "Steiner names five skills: 1) knowing your feelings, their causes and intensity; 2) empathic sensitivity — “emotional resonance”; 3) managing emotions — strengthening positive ones and expressing negative ones constructively; 4) taking responsibility for emotional harm — apologising and making amends; 5) emotional interactivity — using all the skills together in complex situations.\n\n"
                    "Steiner argues that childhood experiences weaken many people’s ability to express feelings freely, but it can be restored through transactional analysis exercises. Suppressing feelings does not destroy them — it leads to psychological problems.\n\n"
                    "Emotional literacy builds personal power, improves relationships and develops social adaptation. Goleman’s (1995) conclusion: managing emotions means not suppressing them but recognising and consciously directing them. Every topic of this course leads to exactly this result — being able to give yourself psychological help.",
                ),
            },
            {
                "kind": "quiz",
                "title": ("Test: Emotsional savodxonligim", "Test: Emocional sawatlılıǵım", "Тест: моя эмоциональная грамотность", "Test: my emotional literacy"),
                "body": TEST_INTRO,
                "results": (
                    (
                        "His-tuyg‘ularni ifodalash va kechirim so‘rash sizga qiyin. Kichikdan boshlang: bugun yaqin odamingizga uning siz uchun nimasi qadrli ekanini ayting.",
                        "Sezimlerdi bildiriw hám keshirim soraw sizge qıyın. Kishiden baslań: búgin jaqın adamıńızǵa onıń siz ushın nesi qádirli ekenin aytıń.",
                        "Вам трудно выражать чувства и извиняться. Начните с малого: сегодня скажите близкому человеку, чем он вам дорог.",
                        "Expressing feelings and apologising is hard for you. Start small: today tell someone close to you what you value about them.",
                    ),
                    (
                        "Sizda yaxshi emotsional savodxonlik bor. Javobgarlik ko‘nikmasini mustahkamlang: xato qilganingizda «lekin» so‘zisiz kechirim so‘rashni mashq qiling.",
                        "Sizde jaqsı emocional sawatlılıq bar. Juwapkershilik kónlikpesin bekkemleń: qáte qılǵanıńızda «biraq» sózisiz keshirim sorawdı shınıqtırıń.",
                        "У вас хорошая эмоциональная грамотность. Укрепите навык ответственности: тренируйтесь извиняться без слова «но».",
                        "You have good emotional literacy. Strengthen responsibility: practise apologising without the word “but”.",
                    ),
                    (
                        "Ajoyib! Siz his-tuyg‘ularingizni yurak bilan boshqarasiz. Siz o‘zingizga ham, boshqalarga ham psixologik yordam bera olasiz.",
                        "Ájayıp! Siz sezimlerińizdi júrek penen basqarasız. Siz ózińizge de, basqalarǵa da psixologiyalıq járdem bere alasız.",
                        "Отлично! Вы управляете эмоциями с сердцем. Вы можете оказывать психологическую поддержку и себе, и другим.",
                        "Excellent! You manage your emotions with heart. You can give psychological support both to yourself and to others.",
                    ),
                ),
                "questions": [
                    (("Yaqinlarimga ularni yaxshi ko‘rishimni yoki qadrlashimni so‘z bilan aytaman.", "Jaqınlarıma olardı jaqsı kóretuǵınımdı yamasa qádirleytuǵınımdı sóz benen aytaman.", "Я говорю близким словами, что люблю и ценю их.", "I tell the people close to me in words that I love and value them."), FREQ),
                    (("Iliq so‘z yoki maqtovni noqulay sezmasdan qabul qila olaman.", "Jıllı sóz yamasa maqtawdı ıńǵaysızlanbay qabıllay alaman.", "Я могу принять тёплые слова или похвалу без неловкости.", "I can accept kind words or praise without feeling awkward."), FREQ),
                    (("Xato qilsam, bahona qidirmasdan kechirim so‘rayman.", "Qáte qılsam, sıltaw izlemey keshirim sorayman.", "Если я ошибся, я извиняюсь, не ища оправданий.", "When I make a mistake, I apologise without making excuses."), FREQ),
                    (("Xafa bo‘lsam, buni ochiq aytmasdan, kinoya yoki sukut bilan bildiraman.", "Renjisem, bunı ashıq aytpay, kekesin yamasa úndemew menen bildiremen.", "Если обижаюсь, я не говорю прямо, а показываю это сарказмом или молчанием.", "When hurt, I don’t say it openly but show it with sarcasm or silence."), FREQ_R),
                    (("O‘zimni kamchiliklarim bilan qabul qilaman.", "Ózimdi kemshiliklerim menen qabıllayman.", "Я принимаю себя вместе со своими недостатками.", "I accept myself along with my flaws."), FREQ),
                ],
            },
            {
                "kind": "cards",
                "title": ("Amaliy mashq: Savodxon iboralar", "Ámeliy shınıǵıw: Sawatlı sóz dizbekleri", "Практика: грамотные фразы", "Practice: literate phrases"),
                "body": (
                    "«Kechirasan, lekin sen ham...» | «Kechirasan. Men noto‘g‘ri qildim va seni xafa qildim. Buni qanday tuzatay?»\n«Menga baribir» (aslida xafa bo‘lsangiz) | «Bu gap meni xafa qildi. Gaplashib olsak bo‘ladimi?»\n«Yig‘lama, arzimaydi» | «Ko‘rib turibman, senga og‘ir. Yoningdaman»\nMaqtovga: «Yo‘g‘e, hech narsa emas» | «Rahmat, eshitish juda yoqimli»\n«Sen meni jahlimni chiqarding» | «Men jahldorman, chunki menga ... muhim edi»\nIndamay xafa bo‘lib yurish | His-tuyg‘u va ehtiyojni aniq aytish — Steinerning 1- va 3-ko‘nikmasi",
                    "«Keshir, biraq sen de...» | «Keshir. Men nadurıs islep, seni renjittim. Bunı qalay dúzeteyin?»\n«Maǵan bárbir» (shınında renjigen bolsańız) | «Bul gáp meni renjitti. Sóylesip alsaq bola ma?»\n«Jılama, arzımaydı» | «Kórip turman, saǵan awır. Qasıńdaman»\nMaqtawǵa: «Joq-aw, hesh nárse emes» | «Raxmet, esitiw júdá jaǵımlı»\n«Sen meniń ashıwımdı keltirdiń» | «Men ashıwlıman, sebebi maǵan ... áhmiyetli edi»\nÚndemey renjip júriw | Sezim hám mútájlikti anıq aytıw — Steinerdiń 1- hám 3-kónlikpesi",
                    "«Извини, но ты тоже…» | «Прости. Я поступил неправильно и обидел тебя. Как мне это исправить?»\n«Мне всё равно» (когда на самом деле обидно) | «Эти слова меня задели. Можем поговорить?»\n«Не плачь, ерунда» | «Вижу, тебе тяжело. Я рядом»\nНа похвалу: «Да ладно, ничего особенного» | «Спасибо, очень приятно это слышать»\n«Ты меня разозлил» | «Я злюсь, потому что мне было важно …»\nМолча носить обиду | Ясно назвать чувство и потребность — 1-й и 3-й навыки Штайнера",
                    "“Sorry, but you also…” | “I’m sorry. I was wrong and I hurt you. How can I make it right?”\n“I don’t care” (when you’re actually hurt) | “That hurt me. Can we talk?”\n“Don’t cry, it’s nothing” | “I can see this is hard for you. I’m here”\nTo praise: “Oh, it was nothing” | “Thank you, that’s really nice to hear”\n“You made me angry” | “I’m angry because … mattered to me”\nSilently holding a grudge | Clearly naming the feeling and need — Steiner’s skills 1 and 3",
                ),
            },
            {
                "kind": "reflection",
                "title": ("O‘zingizga yordam: kursdan keyin", "Ózińizge járdem: kurstan keyin", "Помоги себе: после курса", "Self-help: after the course"),
                "body": (
                    "Kursning sakkiz mavzusini eslang. Qaysi ko‘nikma sizga eng ko‘p yordam beradi? Keyingi qiyin paytda o‘zingizga psixologik yordam berish uchun qiladigan uchta aniq qadamingizni yozing.",
                    "Kurstıń segiz temasın eslań. Qaysı kónlikpe sizge eń kóp járdem beredi? Keyingi qıyın waqıtta ózińizge psixologiyalıq járdem beriw ushın isleytuǵın úsh anıq qádemińizdi jazıń.",
                    "Вспомните восемь тем курса. Какой навык поможет вам больше всего? Запишите три конкретных шага, которые вы сделаете, чтобы помочь себе в следующий трудный момент.",
                    "Look back at the eight topics. Which skill will help you most? Write three concrete steps you’ll take to give yourself psychological help in your next difficult moment.",
                ),
            },
        ],
    },
]


EI_TOPICS = TOPICS_1 + TOPICS_2 + TOPICS_3
