"""Build WordPress block content for the Mental Survival sub-pages (translated from mental-survival.com).

Run: python3 build.py  -> writes pages.json next to this file.
Each page: slug, title, excerpt, content (block markup). Parent page is Mental Survival (ID 137).
"""
import html
import json
import os

SITE = "https://www.primordial-protocol.com"


def P(t, cls=None):
    if cls:
        return f'<!-- wp:paragraph {{"className":"{cls}"}} -->\n<p class="{cls}">{t}</p>\n<!-- /wp:paragraph -->'
    return f"<!-- wp:paragraph -->\n<p>{t}</p>\n<!-- /wp:paragraph -->"


def LEAD(t):
    return f'<!-- wp:paragraph {{"fontSize":"large"}} -->\n<p class="has-large-font-size">{t}</p>\n<!-- /wp:paragraph -->'


def H2(t):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{t}</h2>\n<!-- /wp:heading -->'


def H3(t):
    return f'<!-- wp:heading {{"level":3}} -->\n<h3 class="wp-block-heading">{t}</h3>\n<!-- /wp:heading -->'


def UL(items):
    li = "".join(f"<!-- wp:list-item -->\n<li>{i}</li>\n<!-- /wp:list-item -->" for i in items)
    return f'<!-- wp:list -->\n<ul class="wp-block-list">{li}</ul>\n<!-- /wp:list -->'


def OL(items):
    li = "".join(f"<!-- wp:list-item -->\n<li>{i}</li>\n<!-- /wp:list-item -->" for i in items)
    return f'<!-- wp:list {{"ordered":true}} -->\n<ol class="wp-block-list">{li}</ol>\n<!-- /wp:list -->'


def Q(t, cite=None):
    c = f"<cite>{cite}</cite>" if cite else ""
    return (f'<!-- wp:quote -->\n<blockquote class="wp-block-quote"><!-- wp:paragraph -->\n<p>{t}</p>\n'
            f"<!-- /wp:paragraph -->{c}</blockquote>\n<!-- /wp:quote -->")


def IMG(mid, src, alt, cls="pp-photo"):
    return (f'<!-- wp:image {{"id":{mid},"sizeSlug":"large","linkDestination":"none","className":"{cls}"}} -->\n'
            f'<figure class="wp-block-image size-large {cls}"><img src="{src}" alt="{html.escape(alt)}" class="wp-image-{mid}"/></figure>\n'
            f"<!-- /wp:image -->")


def COVER(mid, src, alt, body):
    """Book cover on the left, text on the right (same layout as the Mental Survival page)."""
    return ('<!-- wp:columns {"style":{"spacing":{"blockGap":{"left":"var:preset|spacing|50"}}}} -->\n'
            '<div class="wp-block-columns"><!-- wp:column {"width":"34%"} -->\n'
            '<div class="wp-block-column" style="flex-basis:34%">'
            + IMG(mid, src, alt, "pp-cover") +
            '</div>\n<!-- /wp:column -->\n\n<!-- wp:column -->\n<div class="wp-block-column">'
            + "\n\n".join(body) +
            "</div>\n<!-- /wp:column --></div>\n<!-- /wp:columns -->")


def BTNS(*btns):
    out = []
    for label, url, outline in btns:
        if outline:
            out.append('<!-- wp:button {"className":"is-style-outline"} -->\n<div class="wp-block-button is-style-outline">'
                       f'<a class="wp-block-button__link wp-element-button" href="{url}">{label}</a></div>\n<!-- /wp:button -->')
        else:
            out.append(f'<!-- wp:button -->\n<div class="wp-block-button"><a class="wp-block-button__link wp-element-button" href="{url}">{label}</a></div>\n<!-- /wp:button -->')
    return '<!-- wp:buttons -->\n<div class="wp-block-buttons">' + "".join(out) + "</div>\n<!-- /wp:buttons -->"


def NOTE(t):
    return P(t, "pp-fine")


MS = "/projects/mental-survival"
U = SITE + "/wp-content/uploads/2026/10/"

pages = []


def page(slug, title, excerpt, *blocks):
    pages.append({"slug": slug, "title": title, "excerpt": excerpt, "content": "\n\n".join(blocks)})


# 1. The book ---------------------------------------------------------------
page(
    "the-book", "Mental Survival: The Book",
    "Mental Survival (Hoepli, 2016), Fabrizio Nannini's practical manual on the psychology of individual and group emergencies.",
    COVER(169, U + "mental-survival-book-cover.jpg", "Cover of Mental Survival (Hoepli, 2016)", [
        LEAD("Have you ever sensed serious danger, or felt that you were at risk? Have you ever been frozen by panic over something that happened to you? Have you found yourself in moments of great confusion, close to losing control?"),
        P("Mental survival is about understanding the mechanisms behind these reactions and learning how to face them."),
        P("<em>Mental Survival: a practical manual for individual and group emergencies</em> (Hoepli, 2016) is a reference text on the psychology of survival, for individuals and groups, in any setting. It draws on and summarizes international research ranging from neurobiology to crowd dynamics."),
    ]),
    P("Written to be clear and accessible, it explains what happens inside us when we face danger and how to manage it, including in the everyday situations where these mechanisms are too often underestimated."),
    P("It includes interviews and exclusive contributions from Alex Zanardi, Cody Lundin, Marco Confortola, Alex Bellini, Les Stroud, Mykel Hawke and many other athletes: remarkable examples of resilience and exceptional survivors."),
    H2("The author"),
    P("Fabrizio Nannini is a certified mental coach and survival instructor. A long-time outdoor practitioner, he has made long solo treks in every climate and condition. He teaches mental survival in both outdoor and urban settings and has trained in neurobiology and psychological first aid."),
    NOTE("Published in Italian by Hoepli."),
    BTNS(("Find it on Amazon", "http://amzn.to/1VWXhWG", False), ("Survival For Dummies", MS + "/survival-for-dummies/", True)),
)

# 2. Survival For Dummies ---------------------------------------------------
page(
    "survival-for-dummies", "Survival For Dummies",
    "Survival For Dummies (Hoepli, 2024), Fabrizio Nannini's practical survival manual focused on problem solving and decision making in a crisis.",
    COVER("__SFD_ID__", "__SFD_SRC__", "Cover of Survival For Dummies (Hoepli, 2024)", [
        LEAD("<em>Survival For Dummies</em> (Hoepli, 2024) is Fabrizio Nannini's second book."),
        P("It covers survival across the board, in any setting, climate or situation, with a focus on what matters most in a crisis: problem solving and decision making."),
        P("It's meant as a practical manual for anyone who takes their own safety, and that of their loved ones, seriously, in every situation they might face. Deliberately broad, direct, clear and structured."),
    ]),
    NOTE("Published in Italian by Hoepli in the Wiley <em>For Dummies</em> series."),
    BTNS(("Find it on Amazon", "https://amzn.to/45yONwM", False), ("Mental Survival: the book", MS + "/the-book/", True)),
)

# 3. Coaching ---------------------------------------------------------------
page(
    "coaching", "Coaching",
    "What coaching is, how we work and how a coaching path starts: listening, assessment, a plan, and practical tools.",
    Q("Coaching is partnering with clients in a thought-provoking and creative process that inspires them to maximize their personal and professional potential.", "International Coaching Federation (ICF)"),
    Q("A collaborative, solution-focused, results-oriented and systematic process in which the coach facilitates the enhancement of work performance, life experience, self-directed learning and personal growth of the coachee.", "Association for Coaching"),
    Q("Performance equals potential minus interference: P = p &minus; i.", "W. Timothy Gallwey, <a href=\"https://amzn.to/2X1d9NU\">The Inner Game of Tennis</a>"),
    P("Mental Training, Inc. describes coaching as teaching skills that prevent slumps, blocks and fears, to build mental resilience and perform at your best."),
    P("We could go on quoting the world's leading coaching experts for hours. So here is our own definition:"),
    Q("A practical, fast, collaborative process of transformative growth for the individual, built on reframing beliefs, aimed at better self-knowledge, at developing one's potential and at improving relationships with others."),
    P("There's no standard procedure in our toolkit, because there's no standard person. What we do know how to do:"),
    UL([
        "listen very carefully: to people, problems, situations, goals and previous attempts;",
        "assess the individual and the group with a tailored set of psychometric tests;",
        "dig into the issues raised and analyze what lies underneath;",
        "build an action plan;",
        "act with whatever tools are needed (NLP, mindfulness, games, assignments and more).",
    ]),
    P("Our goal is to support positive change through self-knowledge, awareness of emotions, stress management and deep, consistent work on oneself. But a few things need to be there first:"),
    UL([
        "awareness that there are things to improve;",
        "a sincere wish to change, by your own choice and not because someone else demands it;",
        "the courage to seriously question yourself.",
    ]),
    P("A coaching path starts with a preliminary conversation to check:"),
    UL([
        "whether we can help, and how likely the work is to be effective;",
        "the fit between coach and client;",
        "timing and format.",
    ]),
    P("Coaching is not psychotherapy: when something calls for a clinician, we say so."),
    P("Get in touch to see whether we can start working together. Sessions are available in person in Milan, at your location, or online by video call."),
    BTNS(("Write to us", "/contact/?topic=coaching", False), ("Profiling and psychometric tests", MS + "/profiling/", True)),
)

# 4. Profiling ----------------------------------------------------------------
page(
    "profiling", "Profiling and Psychometric Tests",
    "Personality, emotional intelligence and behavioral tests, tailored to individuals and teams, used as a starting point for conversation and growth, never as labels.",
    P("&ldquo;Know thyself&rdquo; was inscribed at the Temple of Apollo at Delphi, in ancient Greece."),
    P("Knowing who we are, how we relate to others, how empathetic we are and how we perform under stress is the foundation for understanding our real potential and aspirations, at work and in personal growth."),
    P("Sorting the countless nuances of the human mind into categories, or labeling them, has been the dream of great thinkers since antiquity. As far back as ancient Greece, the theory of the four temperaments tried to make certain features of the psyche easier to understand and predict. Summarizing a few traits to grasp others more quickly is a desire as old as humanity itself."),
    P("Today there are many tests based on the work of leading 20th-century psychologists and contemporary researchers. Used well, they describe a person's main behavioral patterns and personality traits."),
    P("We tailor these tests to the individual and to the team, to bring out the differences between people and put them to good use. They come as single tests or as packages, depending on what you want to explore and how much depth you need."),
    H3("What these tests can bring to light"),
    UL([
        "how a person takes in and processes information;",
        "what they base their decisions on;",
        "their degree of empathy;",
        "how they relate to others and work in a team;",
        "emotional intelligence (EQ);",
        "their main personality traits.",
    ]),
    H3("What they're for"),
    UL([
        "recognizing everyone's strengths and facing their weak spots;",
        "understanding relationships in the workplace, so that subgroups can be structured well.",
    ]),
    H2("The tests we offer"),
    OL([
        "<strong>Personality type</strong>, Jungian-derived, in the family of the Myers-Briggs Type Indicator&reg; (MBTI&reg;), the Keirsey Temperament Sorter&reg; and the Montgomery temperament model.",
        f"<strong>Emotional intelligence (EQ)</strong>: how well a person empathizes with others and manages their own emotions and relationships. See <a href=\"{MS}/emotional-intelligence/\">Emotional intelligence</a>.",
        "<strong>Big Five</strong>: the relative weight of five broad personality traits.",
        "<strong>VAK</strong>: preferred communication channels (visual, auditory, kinesthetic). Useful to start a conversation about preferences; research does not support the idea that people learn better when taught in their preferred channel.",
        "<strong>DISC</strong>: behavioral patterns across four broad areas.",
        "<strong>Mindset test</strong>, based on the work of Carol Dweck, professor of psychology at Stanford University: two broad attitudes toward the possibility of personal change.",
    ]),
    P(f"The <a href=\"{MS}/six-seconds/\">Six Seconds</a> tools deserve a separate mention: a well-developed set of instruments for assessing and developing emotional intelligence."),
    P("These and other tests only become meaningful and useful when the results are analyzed one by one, in depth, and discussed with the person, so that the many shades of each of us come together into a realistic picture. Used this way, they are a solid starting point for targeted personal development."),
    H2("Q&amp;A"),
    H3("Why test with us?"),
    P("Because we're not tied to a single testing method. Interpretation is partly shaped by the method, so using several different ones helps us see more areas of a personality, more clearly and completely. Results stay between you and us: we don't share them with anyone else (tests taken online are processed on the publisher's own platform). A synoptic reading gives both the big picture and the detail."),
    H3("Why are some questions repeated?"),
    P("To reduce the statistical chance of error: the more items there are, the smaller the impact of misreading one or two questions."),
    H3("Can the results be faked?"),
    P("In principle, anyone can answer the way they'd like to be seen, and no self-report questionnaire can fully prevent it. But there are no right or wrong answers, so there's little to gain: honest answers give the most useful picture."),
    H3("Are the results reliable?"),
    P("It depends on the instrument. The Big Five model and the TEIQue have strong research support; type-based tools in the MBTI family are widely used in organizations but have weaker evidence of consistency over time. That's why we use all of them as a starting point for conversation, never as fixed labels."),
    BTNS(("Ask about an assessment", "/contact/?topic=psychometric", False), ("Tests for kids and teens", MS + "/personality-tests-for-kids/", True)),
)

# 5. Kids -----------------------------------------------------------------------
page(
    "personality-tests-for-kids", "Personality Tests for Kids and Teens",
    "The MMTIC®, a Jungian personality-type instrument for children and teenagers aged 7 to 17, administered by a certified facilitator with parents.",
    P("There are plenty of personality tests for adults. But how can we better understand our children? How can we understand their personality types, so we can relate to them in the best way? How do they relate to others, and how can we help them fit into groups more naturally? How can we really see the traits that make them unique?"),
    P("The Myers-Briggs Type Indicator&reg; (MBTI&reg;), developed from the 1940s onward from a 1921 work by Carl Jung, is a psychometric questionnaire that describes personality type through a few key dimensions: how we relate to others, how we take in information, how we process it and how we make decisions."),
    P("It's used by (literally) millions of people worldwide, for practical reasons: it's simple, quick to apply, and its results are easy to put to use."),
    P("Because of how it's built, it suits adults, who can complete it with a few basic instructions. That same structure makes it unsuitable for minors."),
    P("From the MBTI came the <a href=\"https://www.peoplestripes.org/take-mmtic-assessment/?parents\">Murphy-Meisgeier Type Indicator for Children&reg; (MMTIC&reg;)</a>, used in many American schools for over twenty years. Like the MBTI it's based on Jung's personality types, but it's simpler in form and is administered differently. It takes into account the fundamental differences of a young respondent and requires an officially certified facilitator to guide the child, together with the parents, through the simple questions and through the all-important feedback session that checks the result. On <a href=\"https://www.youtube.com/channel/UCMKL-BvdjOSmXP7DvN4Lb-Q\">this YouTube channel</a> you can watch the author of the MMTIC&reg; guiding a child through the process and the feedback."),
    P("What you get from a test like this is a picture of your child's natural preferences and character traits, in both logical and more emotional thinking. For ages 7 to 17 there are three versions, designed for different stages of development."),
    H2("How it works"),
    OL([
        "Introducing the interview to the child, making clear that there are <strong>no</strong> right or wrong answers, that they should answer for how they feel (not how they'd like to be), and that it is <strong>not</strong> an evaluation.",
        "Completing the questionnaire together, without influencing the child but explaining the simple questions with practical examples.",
        "Scoring, done online, and analysis by the facilitator.",
        "Checking the results with the child, to see whether the test differs from how they see themselves.",
        "Final review: strengths and possible areas for growth.",
    ]),
    P("Results are given to the child and parents right after the final step. More information, including costs, is on the official site of the <a href=\"https://www.capt.org/assessment-mmtic/children-assessment-personality.htm\">Center for Applications of Psychological Type (CAPT)</a> and its partner site <a href=\"https://www.peoplestripes.org\">People Stripes</a>."),
    P("Fabrizio Nannini is an MMTIC&reg; facilitator certified by CAPT&reg;."),
    BTNS(("Ask about the MMTIC®", "/contact/?topic=psychometric", False), ("Profiling and psychometric tests", MS + "/profiling/", True)),
)

# 6. Emotional intelligence -------------------------------------------------------
page(
    "emotional-intelligence", "Emotional Intelligence",
    "What emotional intelligence is, how it can be assessed (Six Seconds, TEIQue) and why it's worth testing: a starting point, not a verdict.",
    P("How might we define emotional intelligence? A common definition describes it as the ability to recognize, use, understand and consciously manage our own emotions and those of others."),
    P("For years, the market for psychometric testing of human abilities was dominated by the intelligence quotient (IQ), implicitly giving it a huge role in how people were judged, regardless of many other characteristics. It then became clear that &ldquo;traditional&rdquo; intelligence explains only part of what matters in very important areas of life, such as emotional well-being, self-esteem, emotional reactivity and relationships, to name a few."),
    P("In 1995 Daniel Goleman threw a stone into the pond: his book <em>Emotional Intelligence</em> made people aware of how much emotions matter in decisions and in everyday life. The book is a lively tour of the practical advantages of emotional intelligence, its applications in every area of life, and the best ways (at least as of 1995) to measure it and make the most of it. Some of its bolder claims have since been debated by researchers, but the core idea has stuck."),
    P(f"Several assessment methods have been developed since, such as the widely used <a href=\"{MS}/six-seconds/\">Six Seconds</a> model and the more research-grounded TEIQue (Trait Emotional Intelligence Questionnaire). Both give a clear picture of a person's strengths across the many components of emotional intelligence, and of the areas where they could work constructively to balance their skills."),
    H2("Why test your emotional intelligence?"),
    UL([
        "because the questions themselves make us stop and question ourselves;",
        "to better understand our emotional processes, and therefore our decisions;",
        "to understand how we relate to others;",
        "to understand ourselves and others better;",
        "to learn how our emotions evolve in certain situations;",
        "to better understand our children;",
        "to manage our emotional responses better;",
        "to make better use of our abilities and improve where we're weaker.",
    ]),
    P("The emotional intelligence assessments we offer are a practical tool for improving our relationship with ourselves, in social life and at work. The results are <strong>not</strong> an evaluation but an exploration: the starting point for real improvement."),
    BTNS(("Ask about an EQ assessment", "/contact/?topic=psychometric", False), ("Six Seconds assessments", MS + "/six-seconds/", True)),
)

# 7. Six Seconds -----------------------------------------------------------------
page(
    "six-seconds", "Six Seconds EQ Assessments",
    "Six Seconds emotional intelligence assessments (SEI): the reports available and how the debrief turns results into practical strategies.",
    P("<a href=\"https://www.6seconds.org\">Six Seconds</a> is a global network dedicated to emotional intelligence research and assessment. Its simple, clear model looks at how, when and where we make the best use of this remarkable quality, which we can (and should) put at the service of our rational side."),
    P("Six Seconds assessments give a detailed analysis of a person's emotional profile, with a focus on how to improve, in practice, the less efficient areas and bring them into balance with our strengths."),
    P("The questionnaire takes about ten minutes to complete, comes with reliability and validity data published by Six Seconds, and produces several types of report."),
    H2("The main reports"),
    UL([
        "<strong>SEI AV Development</strong>: the most widely used and complete emotional intelligence report.",
        "<strong>SEI AV Leadership</strong>: a more business-oriented version of the Development report.",
        "<strong>SEI YV</strong>: similar to the Development report, designed for young people aged 8 to 18.",
        "<strong>Brain Profiles</strong>: three visual, at-a-glance reports summarizing strengths and weak spots in emotional behavior.",
        "<strong>SEI 360&deg;</strong>: self-assessment combined with feedback from a chosen group of people around you, to compare how you see yourself with how others see you, in their own words.",
    ]),
    P("What the test really does, or rather the debrief session where the profiler goes through the report with you (at least one hour per person), is to look at your strengths and weak points together and, above all, to work out practical strategies for the areas to work on first (empathy, self-awareness, goals, relationships), so you can develop your emotional skills in a concrete way."),
    BTNS(("Ask about a Six Seconds assessment", "/contact/?topic=psychometric", False), ("Emotional intelligence", MS + "/emotional-intelligence/", True)),
)

# 8. Team building ---------------------------------------------------------------
page(
    "team-building", "Team Building",
    "Outdoor team building that takes colleagues out of their usual roles and comfort zones, from Italian forests to Lapland and the African savanna.",
    P("In human resources, team building is a set of training activities, variously called team games, team experiences or team wellbeing (playful, experiential or wellness-oriented), whose purpose is to form a group of people. That's the textbook definition: precise, if rather clinical."),
    P("But what is team building really for? Why are more and more companies investing in it?"),
    P("Strictly speaking, &ldquo;building&rdquo; may not be the right word: it suggests constructing something from scratch, yet how many work teams have been together for years and just need a tune-up? Creating a team from zero is one thing; improving an existing one by bringing out the best in its members, so they can express their full potential, is a different matter, and a harder one."),
    P("As in any relationship, the bond needs feeding: empathy, changing perspective, putting yourself in others' shoes and contributing to an exchange that benefits everyone. In teamwork too, synergy and communication between members need regular maintenance, toward individual and collective growth."),
    P("In teams, our beliefs about people often lag behind how those people have actually grown: what we think of someone may not change at the same pace as the person does."),
    P("Stepping out of standard work patterns and experiencing colleagues in other roles, and above all outside the comfort zone, is key to resetting our mental models of the people we share our working days with."),
    P("More and more authors recognize emotional intelligence as a set of skills complementary to purely cognitive abilities. Daniel Goleman (<em>Working with Emotional Intelligence</em>, 1998) names five core emotional and social competencies:"),
    OL(["self-awareness", "self-regulation", "motivation", "empathy", "social skills"]),
    P("Developing these competencies through physical and sports activities, including extreme ones, individual or in groups, is the basis of our training programs."),
    IMG(166, U + "pure-survival-group-forest.jpg", "A group training outdoors in a forest"),
    P("Our style is distinctly outdoor: outside the comfort zone of the workplace and outside traditional patterns and roles, we encourage change by stimulating creativity and empathy, reaching results as a team and turning old dynamics upside down. The aim is to reach a goal together, where everyone really matters and is encouraged to contribute with everything they have."),
    H2("Where we do it"),
    P("It could be a forest in Italy, or the shore of a mountain lake. Or the cold of Lapland, driving a team of Alaskan huskies and sleeping under an unforgettable aurora borealis. Or walking and surviving in the heat of the savanna or an African jungle."),
    IMG(179, U + "pure-survival-kenya.jpg", "On the trail in Kenya"),
    P("Every option is proposed after assessing the needs of the client and the team. Everything is documented and filmed, so you have a record and a memory of the activities and the emotions."),
    P("Our work comes in several forms: from a simple incentive trip, to a more structured outdoor training program, to a true immersive team building, (really) 24 hours a day, designed for results on the group and on each person that are concrete, lasting and, above all, useful. When do you want to leave?"),
    BTNS(("Plan a team building", "/contact/?topic=team-building", False), ("Pure Survival", "/projects/pure-survival/", True)),
)

# 9. Forest therapy --------------------------------------------------------------
page(
    "forest-therapy", "Forest Therapy",
    "Guided, mindful time among the trees inspired by Japanese shinrin-yoku: who it's for, how it works, and what the research does and doesn't show.",
    P("Forest therapy grew out of <em>shinrin-yoku</em> (&ldquo;forest bathing&rdquo;), a practice promoted in Japan since the 1980s. It involves mindful, structured time in woodland, following particular methods, in places chosen for their trees and their atmosphere. Alongside this contact with nature, participants do awareness exercises to bring attention to the present and actively engage all the senses in the place where they are. Researchers have been studying it for decades, and it has a growing number of practitioners around the world."),
    IMG(166, U + "pure-survival-group-forest.jpg", "A group walking slowly in the forest"),
    P("<strong>Who is it for?</strong> Everyone. It can be especially valuable for people who don't live in contact with nature and who live or work mostly in cities."),
    P("<strong>How does it work?</strong> In a group, with a guide leading a walk through carefully chosen green areas and teaching breathing and multisensory awareness techniques, adapted to each situation and setting."),
    P("<strong>How long does it last?</strong> Half a day, a full day, or several days in a row. Time in green areas is planned around each person's needs and the group's availability."),
    P("<strong>What happens, in practice?</strong> Some trees release aromatic compounds, called phytoncides, that we breathe in during the walk; researchers have studied their possible effects on stress and on immune markers, with promising but still preliminary results. Soft, filtered light and the sound of leaves are relaxing for most people, and the breathing and multisensory techniques help us connect with ourselves, here and now. Many people come home feeling more alive, pleasantly slowed down, more present and aware."),
    H2("Why it matters now"),
    P("Humans have become an urban species: more than half of the world's population now lives in urban areas, far from the woods and green spaces where we lived for almost all of our history as a species. This change happened far too quickly for us to fully adapt, and the mismatch has real costs."),
    P("We are more and more disconnected from nature. Cities rarely have as much green space as they need, because parks are costly to maintain and often lose out to uses seen as more important, or more profitable. The public garden has become a place we hurry through rather than a place to stop or meet. Technology has become woven into every part of our routines: we look around less and check our phones more, out of both need and habit."),
    P("It was in response to this kind of disconnection that, in 1982, Japan's Forestry Agency began promoting &ldquo;forest bathing&rdquo; to bring people out of cities and back in touch with nature."),
    H2("What the research says"),
    P(f"The research has grown quickly: dozens of studies, mostly small and short-term, have found encouraging effects on stress, mood and some physiological markers, such as blood pressure. The evidence is promising, not conclusive, and that's how we present it. <a href=\"{MS}/forest-therapy-benefits/\">Read a summary of the main findings and their limits</a>."),
    P(f"There's also growing interest in bringing some of these benefits indoors, into homes and workplaces: see <a href=\"{MS}/indoor-forest/\">Indoor Forest</a>."),
    P("The forest bathing sessions and programs we run are simple, engaging, accessible to everyone and inexpensive."),
    NOTE("Forest bathing is a well-being practice, not a medical treatment, and it doesn't replace medical care."),
    BTNS(("Ask about a forest session", "/contact/?topic=retreats", False), ("The benefits: what the research says", MS + "/forest-therapy-benefits/", True)),
)

# 10. Forest therapy benefits --------------------------------------------------------
page(
    "forest-therapy-benefits", "The Benefits of Forest Therapy: What the Research Says",
    "Five areas where forest bathing has been studied (immune markers, blood pressure, stress, the parasympathetic system, mood), with sources and limits.",
    P("What are the real, measurable benefits of forest bathing? Here are five areas researchers have studied, with the sources."),
    P("A word of caution first. Most of these studies are small, often short-term, and many come from a limited number of research groups in Japan. The findings are best read as promising rather than proven."),
    H2("1. Immune function"),
    P("Breathing phytoncides, natural compounds that some trees produce to protect themselves, has been linked to higher activity and numbers of natural killer (NK) cells, part of the immune system's first line of defense. In a series of small studies of healthy Japanese adults who spent three days in forest areas, NK activity rose and stayed higher for more than 30 days after the trip; a city trip of the same length did not have this effect. These are changes in an immune marker in healthy people, not evidence that forest bathing prevents disease."),
    NOTE("Source: Li Q. Effect of forest bathing trips on human immune function. <em>Environ Health Prev Med.</em> 2010;15(1):9&ndash;17."),
    H2("2. Blood pressure"),
    P("High blood pressure is a major risk factor for stroke and heart attack. A systematic review and meta-analysis of 20 trials, with 732 participants in total, found lower systolic and diastolic blood pressure in forest settings than in non-forest settings."),
    NOTE("Source: Ideno Y et al. Blood pressure-lowering effect of Shinrin-yoku (forest bathing): a systematic review and meta-analysis. <em>BMC Complement Altern Med.</em> 2017;17(1):409."),
    H2("3. Stress"),
    P("In field experiments carried out in 24 forests across Japan, walking in or simply viewing a forest was associated with lower cortisol (a stress hormone), lower pulse rate and blood pressure, and greater parasympathetic activity than the same activities in a city. Psychological studies have also reported lower stress and better mood after forest walks."),
    NOTE("Sources: Park BJ et al. The physiological effects of Shinrin-yoku: evidence from field experiments in 24 forests across Japan. <em>Environ Health Prev Med.</em> 2010;15(1):18&ndash;26. Morita E et al. Psychological effects of forest environments on healthy adults. <em>Public Health.</em> 2007;121(1):54&ndash;63."),
    H2("4. The parasympathetic nervous system"),
    P("Stress keeps the &ldquo;fight, flight or freeze&rdquo; response of the sympathetic nervous system switched on. A review of field experiments found that forest bathing was associated with less anxiety and with higher heart rate variability, a sign that the parasympathetic &ldquo;rest and digest&rdquo; system is more active. The authors call the evidence limited but consistent, and note small samples and the lack of a standard forest-bathing protocol."),
    NOTE("Source: Farrow MR, Washburn K. A review of field experiments on the effect of forest bathing on anxiety and heart rate variability. <em>Glob Adv Health Med.</em> 2019;8:2164956119848654."),
    H2("5. Mood and well-being"),
    P("A 2017 review of 64 studies summarized research on forest bathing and nature therapy across several areas, including mood, anxiety and stress, cardiovascular health and pain, and concluded that the practice is a promising complement to conventional care that deserves further study."),
    NOTE("Source: Hansen MM, Jones R, Tocchini K. Shinrin-Yoku (forest bathing) and nature therapy: a state-of-the-art review. <em>Int J Environ Res Public Health.</em> 2017;14(8):851."),
    P("Forest time is a good complement to a healthy life, not a substitute for medical care."),
    BTNS(("Ask about a forest session", "/contact/?topic=retreats", False), ("Forest therapy", MS + "/forest-therapy/", True)),
)

# 11. Indoor Forest ------------------------------------------------------------------
page(
    "indoor-forest", "Indoor Forest (I+F)",
    "I+F (Indoor Forest): biophilic design of workplaces, homes and urban spaces inspired by research on forest bathing.",
    P("I+F stands for <strong>Indoor Forest</strong>: a project to redesign corporate or commercial green spaces, or to design new ones, inspired by the research on forest bathing and grounded in good design."),
    P("Volumes are rebalanced to make room for healthy, natural greenery. Relaxation and smart-working areas are created where technology doesn't dominate and nature is present. Plants are chosen and combined to make spaces more pleasant to breathe and live in. Aromas, essential oils and phytoncides like those of the forests they come from are used. Water flows freely, adding the humidity that's good for breathing and skin, while light and sound support a healthier, more productive working day."),
    P("In collaboration with the architecture studio of Mauro Mazzali, we offer the design or redesign of workplaces, homes and urban areas, creating livable green spaces: places to work well or to decompress during breaks, within an efficient, healthy and ecological system."),
    H2("Biophilia and interior design"),
    P("Bringing the well-being of green elements indoors, supported by the building's central systems, to recreate the microclimate of a natural setting such as a forest or woodland."),
    P("The aim is a stimulating new work environment, healthy and as restorative as possible, so that people genuinely benefit from spending time there: a space they might even prefer to working from home. An environment that supports concentration and lower stress through natural elements."),
    P("Biophilic design can offer good answers to today's challenges in offices. A study by Politecnico di Milano and the University of Genoa on people's well-being during the COVID-19 lockdown found that the features of their homes mattered for their mental and physical health: room size, natural light, acoustic comfort, privacy, the presence of balconies, terraces or gardens, the view outside and indoor air quality. These issues will need to be addressed from now on, and biophilic design is well placed to help."),
    BTNS(("Talk to us about a project", "/contact/?topic=other", False), ("Forest therapy", MS + "/forest-therapy/", True)),
)

# 12. Shamanism -------------------------------------------------------------------------
page(
    "shamanism", "Shamanism",
    "Fabrizio Nannini's personal path in transcultural shamanism: how it started, how he teaches it, and his training. A spiritual practice, not a therapy.",
    IMG(307, SITE + "/wp-content/uploads/2026/11/gabri_sqr.jpg", "Fabrizio Nannini with his son", "pp-portrait"),
    P("I've worked with energy, if we can call it that, for a very long time. My path began with an unstoppable cultural curiosity, sparked by reading Frazer's <em>The Golden Bough</em> at 17. It continued with the anthropological study of ritual, then of transcultural shamanism, the common denominator of human spirituality, and of the healing techniques tied to energy and emotions. That curiosity has never been fully satisfied, because the path of study and learning is endless."),
    P("My training and approach are very rational. I keep testing theories and techniques, to see which of them can help people feel better and which ones I'm able to use."),
    P("It all started with my grandmother. I was six and she was very ill. I wanted with all my heart to make her well, but I had no idea how."),
    P("That will has stayed the same; the skills have grown step by step, day by day. But I want to be clear: I have no special gift. I've simply cultivated concentration, intention and the ability to visualize, qualities that are within everyone's reach and have always been inside us, even if we often don't notice them or don't want to look for them. It's all much simpler than you might think."),
    P("I have no dogmas, and I neither offer nor seek them. I have no certainties, except the purity of my intentions when I agree to try to help someone. I have no explanations for what happens when I work. When a situation is resolved, I'd be lying if I said it was my doing. I have deep respect for something much greater than me, which allows me to work with it and helps me help others."),
    P("To quote the famous Lakota healer Frank Fools Crow, without making comparisons that would be utterly irreverent, perhaps I'm just a &ldquo;hollow bone&rdquo; through which blows a breath of something that doesn't belong to me, but that I somehow manage to use for good."),
    P("For me, what matters is that it works. The how and the why can be debated for years (better after we've made it through, though); what counts is the result."),
    P("Out of deep respect both for indigenous cultures and for my own roots, I avoid any form of cultural appropriation, at least in outward form (clothing and so on). I respect all the cultures that have shaped my training, but I was born in Italy and I dress like it, in every setting. I don't care for people who surround themselves with outward symbols, or who collect experiences like trading cards: searching is one thing, being able to say you've done something just to show it off is another. Life is a journey and a constant search, of course, but collecting &ldquo;single-serving experiences&rdquo; of this or that, without stopping to reflect on how simple what we can do with our own potential really is, is not something I share."),
    P("In my practical shamanism courses I teach a very simple method, which I certainly didn't invent and which has existed for tens of thousands of years. There are no frills or extras. It's an experience to undertake only if you feel, deep down, that you need to; otherwise I'm the first to suggest letting it go. There can be further steps (healing, soul retrieval and so on), to be approached only when you feel ready and after practicing on your own for a while. You learn without hurrying, with time and practice, as it has always been."),
    H2("Training and experience"),
    UL([
        "Seminar &ldquo;The Way of the Shaman&rdquo; with Lorenza Menegoni, translator and student of Michael Harner",
        "Seminar &ldquo;Soul Retrieval&rdquo; with Lorenza Menegoni",
        "Member of the <a href=\"https://shamanism.org/\">Foundation for Shamanic Studies</a>, founded by Michael Harner",
        "Member of the <a href=\"https://shamanicpractice.org/member-directory/fabrizionannini/\">Society for Shamanic Practice</a>",
        "Online courses at the University of New Mexico with Eliseo &ldquo;Cheo&rdquo; Torres on curanderismo (Traditional Healing Using Plants; Traditional Healing of the Mind, Energy &amp; Spirit; Traditional Healing of the Body; Global &amp; Cultural Influences of Traditional Healing)",
        "Study path with Dario Nardi (UCLA) on Scandinavian shamanism",
        "MOOCs at The Chinese University of Hong Kong (Everyday Chinese Medicine I and II) and at The Hong Kong University of Science and Technology (Health Concepts in Chinese Medicine)",
        "Shamanic circles as participant and as leader since 2016",
        "Regular full-immersion courses in transcultural shamanism, smudging with sacred plants, medicine wheel, temazcal and spiritual healing techniques",
        "Regular shamanic journeying, alone and in groups, for knowledge and spiritual healing",
        "Shamanic Reiki; Reiki level 3, practicing extensively since 1996",
        "Study and practice of mindfulness, meditation and lucid dreaming",
        "Advanced study and practice of aromatherapy, shamanic aromatherapy, medicinal plants and curanderismo",
        "Sweat lodge (temazcal or inipi): building and practice",
        "<em>Segnatore</em>, a traditional Italian folk healer, third generation through my family (paternal aunt, father)",
        "Study and practice of Tibetan singing bowls and harmonic overtone singing (sygyt)",
        "Storywell PMAI facilitator on Jungian archetypes (Pearson-Marr method)",
        "Emotional intelligence assessor for the Six Seconds and TEIQue psychometric tests",
        "Mental Survival coach on <a href=\"https://ritualmente.com\">Ritualmente</a>",
        "Psychological First Aid training at Johns Hopkins University (MOOC) and with the NCTSN (The National Child Traumatic Stress Network)",
        "Studies in anthropology, religion and spirituality, myth and symbolism (Jungian orientation)",
        "A rational, analytical approach, open to and looking for what religions, rituals, techniques and practices have in common",
        "Author of a manual on the psychology of survival (<em>Mental Survival</em>, Hoepli, 2016)",
    ]),
    P("Its transcultural approach, free of creeds, dogmas and superstructures, makes shamanism compatible with any religion, with full respect for each person's faith (or lack of it)."),
    P("I live and practice in Milan, but I have a base in the Modena Apennines, in Emilia-Romagna, where I run courses and hold shamanic circles completely immersed in nature (see <a href=\"/projects/pure-survival/\">Pure Survival</a>). My personal spirituality is animistic: I try to bring together the teachings of Taoism and early Buddhism with spiritual techniques from around the world, especially those of the Mesoamerican curanderos and the Lakota. My path of study and growth never ends."),
    NOTE("Shamanism is presented here as a spiritual, cultural and personal practice, documented across many cultures. It is not a medical or psychological treatment and is not a substitute for one."),
    BTNS(("Ask about a course or circle", "/contact/?topic=retreats", False), ("Mental Survival", MS + "/", True)),
)

# 13. Survivability Test ---------------------------------------------------------------
page(
    "survivability-test", "Survivability Test®",
    "The Survivability Test®, a questionnaire on how people tend to respond to emergencies. Take it online (currently in Italian).",
    P("The Survivability Test&reg; is a questionnaire built around how people respond to emergencies: how we tend to react under threat, pressure and uncertainty."),
    P("It's currently available in Italian only. If the form below doesn't load, <a href=\"https://formnx.com/f/11xi12\">open it in a new page</a>."),
    '<!-- wp:html -->\n<div class="pp-embed-form"><iframe src="https://formnx.com/f/11xi12?iframe=true" title="Survivability Test (in Italian)" loading="lazy" allow="clipboard-write"></iframe></div>\n<!-- /wp:html -->',
    BTNS(("Coaching", MS + "/coaching/", False), ("Mental Survival", MS + "/", True)),
)

# 14. Team and approach -----------------------------------------------------------------
page(
    "team", "Team and Approach",
    "Who works on Mental Survival, our approach and our method: practical, results-oriented, built like a survival situation.",
    H2("Our team"),
    P("We're a team of professionals from very different fields: coaches, instructors, educators, university lecturers, authors, psychologists, researchers and experts in NLP and mindfulness, all sharing the wish to help people grow and improve in concrete terms, both professionally and personally. Our approach is unconventional and adapts to every situation, just as every person we work with is a world of their own."),
    H3("Fabrizio Nannini"),
    P("A certified mental coach, trained in Psychological First Aid (Johns Hopkins, 2016), and the author of a manual on the psychology of survival (<em>Mental Survival</em>, Hoepli, 2016). He wrote a survival column for <em>Men's Health</em> Italy and often appears as a consultant on Italian TV programs (Rai and Mediaset). Certified MMTIC&reg; facilitator for the Jungian personality-type instrument for young people aged 7 to 17."),
    H3("Francesco Campiotti"),
    P("A graduate in modern literature with a PhD in personal education and training. Since 2011 he has worked in education and training across many fields. An instructor with the Federazione Internazionale Survival and an outdoor trainer, he has led expeditions on several continents and in many natural environments. He works with several companies as a team builder and trainer."),
    H2("Our approach"),
    P("Entirely practical and aimed at getting the result you want, as quickly as possible, and making it last."),
    P("In pool, sometimes the only way to pot the ball is a bank shot. That's what we do almost every time: we approach the problem from a different angle, focusing only on a positive solution. If we take on a job, it's because we like it, we care about it and we're confident we can make a positive difference. If clients want to work with us, it's because they can see our passion, and that we don't give up easily."),
    H2("Our method"),
    P("In one sentence, borrowing the title of a Woody Allen film: <em>Whatever Works</em>."),
    P("There's no standard approach, because problems never come off an assembly line. But broadly speaking, we proceed the way you would in a survival situation:"),
    UL(["understand where you are;", "assess the resources you have;", "decide where you want to go."]),
    P("On this three-step system we build a simple, structured process, focused entirely on the result to be achieved, without limiting how we get there. Whatever works. As long as the results last."),
    BTNS(("Write to us", "/contact/", False), ("About Fabrizio", "/about/", True)),
)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pages.json")
with open(out, "w") as f:
    json.dump(pages, f, ensure_ascii=False, indent=1)
print(len(pages), "pages ->", out)
