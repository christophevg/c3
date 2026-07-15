# Common Writing Mistakes — Full Taxonomy

**Purpose:** Reference catalog for the `writing-mistakes` skill. Each category lists representative mistakes with the recognized/correct form where one exists. Used to flag hits as `TODO:` notes for the author to fix — never to rewrite the author's prose.

**Source:** Synthesized from Strunk (*Elements of Style*), Orwell (*Politics and the English Language*), Williams (*Style: Toward Clarity and Grace*), Pinker (*The Sense of Style*), Zinsser (*On Writing Well*), journalism/style guides, and non-native-English-learner references. Research conducted 2026-07-13.

## Canonical vs. Craft

Each item is labelled **[CANONICAL]** (a factual correct form exists — flag with the recognized form) or **[CRAFT]** (a judgment call — flag the pattern, author decides) or **[MIXED]** (some items canonical, some craft).

- **CANONICAL** flag format: `TODO: <error type> at <location> — recognized form is X`
- **CRAFT** flag format: `TODO: <pattern name> at <location> — consider whether this is intended`

---

## 1. Sentence-level craft  [MIXED — mostly CRAFT, a few CANONICAL]

Mechanical/grammatical problems at the sentence level that hurt clarity or vigor, independent of word choice.

1. **Passive voice overuse** [CRAFT] — "Mistakes were made" / "It was decided that..." when the actor matters. Flag when the doer is recoverable and relevant but suppressed.
2. **Nominalizations / zombie nouns** [CRAFT] — actions locked into nouns, forcing abstract subjects: "Our lack of knowledge about local conditions precluded determination of committee action effectiveness..." Flag consecutive nominalizations and nominalizations after empty verbs ("conduct an investigation", "give rise to", "exhibit a tendency to").
3. **Weak / auxiliary-heavy verbs** [CRAFT] — "is", "has", "make", "do", "perform", "achieve" carrying the action: "make a decision" (decide), "perform an analysis" (analyze), "have an effect on" (affect).
4. **Adverb overuse** [CRAFT] — redundant adverbs that duplicate the verb: "ran quickly", "completely destroyed", "very unique".
5. **Adjective stacking** [CRAFT] — "rich, vibrant, profound, meticulously crafted" — piled modifiers that add no information.
6. **Redundancy & tautology** [CANONICAL] — "free gift", "end result", "past history", "personal friend", "added bonus", "consensus of opinion", "unexpected surprise", "true facts", "first and foremost". Reduced form: gift / result / history / friend...
7. **Wordiness / convoluted phrasing** [CRAFT] — "due to the fact that" (because), "in order to" (to), "has the ability to" (can), "in the event that" (if), "for the purpose of" (for), "at this point in time" (now). Also Orwell's "verbal false limbs": render inoperative, make contact with, serve the purpose of.
8. **Misplaced modifier** [CANONICAL] — "The script only deletes files older than 30 days." vs "deletes only files older than 30 days." Flag when only/just/even/almost/nearly sits away from what it limits.
9. **Dangling modifier** [CANONICAL] — "To calibrate the sensor, a reference voltage was applied." (implies the voltage calibrated the sensor); "After reviewing the logs, the root cause became obvious." Diagnostic: after an opening comma, is the next word the doer?
10. **Squinting modifier** [CANONICAL] — "Engineers who write documentation rarely get promoted." (rarely = write or get promoted?)
11. **Subject-verb agreement** [CANONICAL] — across long separating phrases: "The list of approved vendors... are posted" (is). Each/every/either/neither/none singular: "Each of the microservices have" (has). "Along with / as well as" do not pluralize a singular subject.
12. **Parallelism errors** [CANONICAL] — series: "ingests raw logs, parsing them, and then it stores..." (ingests, parses, stores). Bullets mixing imperative/passive/gerund. Correlatives: "not only handles... but also it manages" (but also manages). Comparisons: "lower than the old API" (lower than that of the old API).

**Sources:** Strunk, *Elements of Style* (Rules / Misuse); Orwell, *Politics and the English Language*; Williams, *Style: Toward Clarity and Grace*; datafield.dev, *Chapter 6: Sentences That Work*.

---

## 2. Lexical & phrasing  [MIXED]

Word- and phrase-level mistakes beyond the idiom/proverb misuse covered by `writing-idioms`.

1. **Clichés / dying metaphors** [CRAFT] — worn-out figures used to avoid inventing phrasing: "toe the line", "ride roughshod over", "Achilles' heel", "swan song", "hotbed", "grist to the mill", "on the order of the day". Orwell: never use a metaphor you're used to seeing in print. (Flag only the stale/dying variety, not broken idioms — those go to `writing-idioms`.)
2. **Mixed metaphors** [CRAFT] — clashing images: "The Fascist octopus has sung its swan song"; "the jackboot is thrown into the melting pot"; "We'll burn that bridge when we come to it."
3. **Malapropisms** [CANONICAL] — similar-sounding word, nonsensical: "the very pineapple of politeness" (pinnacle), "to languish praise" (lavish), "illiterate him from your memory" (obliterate), "affluence" for "influence".
4. **Eggcorns** [CANONICAL] — plausible-sounding substitutions that stay semantically close: "for all intensive purposes" (for all intents and purposes), "mute point" (moot point), "escape goat" (scapegoat), "old-timer's disease" (Alzheimer's), "doggy-dog world" (dog-eat-dog), "self-refilling prophecies" (self-fulfilling), "chomping at the bit" (champing), "tow the line" (toe the line), "seize and desist" (cease and desist), "could care less" (couldn't care less).
5. **Pleonasms / redundancies** [CANONICAL] — "free gift", "end result", "past history", "personal friend", "added bonus", "advance planning", "unexpected surprise", "unintended mistake", "basic fundamentals", "true facts".
6. **Vague quantifiers** [CRAFT] — "many", "a lot", "numerous", "a number of", "several", "some" without a number or scope. Flag when a concrete figure/scope is recoverable.
7. **Weasel words / hedging** [CRAFT] — empty modifiers that weaken: "actually", "basically", "really", "very", "literally", "virtually", "essentially", "overall", "quite", "truly", "ultimately", "practically", "kind of", "sort of". Distinguished from legitimate qualifying.
8. **Absolute / overclaiming language** [CRAFT] — "always", "never", "everyone", "no one", "the best", "the only way", "proves that", "completely eliminates" — claims that exceed the evidence.
9. **Strunk's commonly misused words** [CANONICAL] — case ("In many cases, rooms were poorly ventilated" → "Many rooms..."), factor, feature, less vs fewer ("less men" → "fewer men"), literally ("literally dead with fatigue" → "almost dead"), most for almost ("most everybody"), possess for have, respective/respectively (usually omittable), state for say, very (use sparingly), while for and/but/although, due to for because of, claim for declare/maintain.
10. **Pretentious diction** [CRAFT] — Latinate words dressing up simple statements: "utilize" (use), "expedite" (hasten), "ameliorate" (improve), "individual" (as noun, person), "constitute", "exhibit", "eliminate", "liquidate"; foreign phrases when an English equivalent exists.
11. **Meaningless words** [CRAFT] — words with no discoverable referent in context: "values", "vitality", "robust", "vibrant", "rich" (as generic praise).

**Sources:** Orwell, *Politics and the English Language*; Strunk, *Words and Expressions Commonly Misused*; Merriam-Webster (eggcorns/malapropisms/redundancies); Grammarly (eggcorns); MLA Style Center (malaprops); Daily Writing Tips (50 redundant phrases).

---

## 3. Non-native English speaker mistakes  [CANONICAL — highest-value for a non-native author]

Errors characteristic of L1 interference, where English has a canonical form the writer missed.

1. **Article misuse (a/an/the, zero article)** — "We developed method to estimate error." → "a method to estimate the error." Omitting articles ("Study was conducted" → "A study..."); adding unnecessary ones; a/an by sound not spelling ("a university", "an hour"). Abstract noncount nouns cause most trouble: evidence, research, literature, information.
2. **Preposition errors** — "interested on" → "interested in"; "dependent of" → "dependent on"; "arrive to" → "arrive at/in"; "discussed this on Section 3" → "in Section 3"; "consistent to" → "consistent with"; "focus about" → "focus on".
3. **False friends / false cognates** — "sensible" (EN prudent) vs "sensible" (FR/ES = sensitive); "actual" (EN real) vs "actual" (ES/FR = current); "fabric" (EN material) vs "fábrica" (ES = factory); "sympathetic" (EN compassionate) vs "sympathique" (FR = nice); "library" (EN borrow) vs "librería/buchhandlung" (bookshop); "eventually" (EN in the end) vs "eventuell" (DE = possibly).
4. **Countable / uncountable noun errors** — "informations", "researches", "advices", "furnitures", "equipments", "luggages", "knowledges", "evidences", "accommodations" (mass noun in EN). "Many" + uncountable; "a/an" + uncountable.
5. **Tense / aspect errors** — present perfect vs past simple: "I have seen him yesterday" → "I saw him yesterday" (definite past time takes past simple); "I am studying here for five years" → "I have been studying here for five years" (extended-now takes perfect). Overusing simple past where present perfect is required.
6. **Wrong verb form after auxiliaries** — "The samples were analyze" → "were analyzed" (past participle after was/were/is/are); "He wants to went home" → "to go"; "warned him not to appeared again" → "not to appear".
7. **Gerund vs infinitive** — "I enjoyed to eat" → "I enjoyed eating" (enjoy/consider/suggest/avoid + gerund); "I want reading" → "I want to read" (want/decide/hope + infinitive); "suggested to go" → "suggested going"; "look forward to hear" → "to hearing".
8. **Collocation errors** — make/do/take/have: "do homework" (not "make homework"), "make a decision" (not "do a decision"), "do research" (not "make research"); "heavy traffic" (not "big traffic"), "bitterly disappointed", "commit a crime" (not "do a crime"). Preposition collocations: "consistent with", "associated with", "increase in risk", "correlated with".
9. **Register mixing** — colloquial phrasal verbs in formal prose ("find out" → "determine", "look into" → "investigate"); overusing present continuous for stable statements ("This paper is presenting..." → "This paper presents..."); over-formal padding ("owing to the fact that" → "because").
10. **Double comparatives / wrong comparison** — "more better", "most biggest", "more easier". "more + comparative" and "-er + -er" cannot stack.
11. **Adjective vs adverb confusion** — "performed good" → "performed well"; "a highly temperature" → "a high temperature"; "runs quick" → "runs quickly".
12. **Direct-translation idioms / calques that don't exist in English** — literal renderings of L1 idioms that are meaningless or wrong in English (calquing "take a decision" from FR/ES where EN prefers "make a decision"; "make a photo" from DE/FR/ES where EN says "take a photo"). Flag when a phrase reads as a literal translation of a non-English idiom.

**Sources:** Trinka.ai, *20 Most Common Grammar Mistakes by Non-Native Speakers*; Editor World, *Common English Mistakes Non-Native Speakers Make*; Collins, *Common Errors in English*; Jama (2022), *Common Errors of Gerundial and Infinitival Forms* (ERIC); Pérez Guerra & Smirnova (2024), *L1 Influence on the Present Perfect*.

---

## 4. Structural & argumentative craft (beyond continuity)  [CRAFT]

Discourse-level craft problems beyond continuity/coherence (covered by `writing-continuity`). Flag the structural weakness; author decides how to fix.

1. **Throat-clearing / empty openings** — "In today's fast-paced world...", "We live in a rapidly changing...", "For years, experts have debated...", "It is important to note that...", "The following section discusses...". Three subtypes: process talk (announcing what you'll do), value signaling (asserting importance instead of demonstrating it), context padding.
2. **Buried lede** — the newsworthy/key point appears in paragraph 4 instead of sentence 1; opening with secondary details before the actual claim.
3. **Topic-sentence drift** — a paragraph whose body no longer matches its opening sentence, or whose topic sentence is buried mid-paragraph.
4. **Unsupported generalizations** — "Many people are concerned about...", "Experts argue that...", "Some critics say...", "It is widely known that..." with no named source, number, or citation. Lazy attribution.
5. **False balance** — giving equal weight to unequal claims; "both sides" framing when one side is factually wrong.
6. **Non sequiturs** — a conclusion that doesn't follow from its premises; a sentence that lands with no logical link to the preceding one (distinct from "missing transition" — flag here when the link is absent because the *logic* is absent, not just unstated).
7. **Circular reasoning** — the claim restates the premise: "X is important because of its importance"; "The model is reliable because it produces reliable results."
8. **Missing evidence links** — a step in the argument is assumed rather than shown; "this clearly demonstrates..." without the demonstration.
9. **Overlong sentences / paragraphs** — sentences past ~40-50 words with no breath; paragraphs over ~150 words with no break. Flag length as a craft signal, not a hard rule.
10. **Empty closings / outline conclusions** — "Despite these challenges, ... faces several challenges...", "Future Outlook", "In conclusion..." recap sections that restate rather than advance.
11. **Curse of knowledge** [CRAFT] — jargon/intermediate steps the writer assumes are obvious; a scene in the writer's mind the reader can't see. Flag undefined terms introduced without orientation, and unexplained intermediate steps.

**Sources:** MLA Style Center (*Don't Bury the Lede*); Trent Lythgoe (*Better Sentences: Throat-clearing*); MasterClass (*Bury the Lede*); River Editor (*Inverted Pyramid / false balance*); Pinker, *The Sense of Style* (curse of knowledge & classic style); Strunk, *Elements of Style* III.

---

## 5. AI / LLM tells (deepen beyond a vocabulary list)  [CRAFT — density is the signal]

Structural/stylistic fingerprints of model-generated prose that go beyond a single-word "ChatGPT smell" vocabulary list (covered by `writing-voice`). The vocabulary list lives there; here flag the *patterns* and *density*.

**Key principle:** Individual phrases aren't the problem — density is. One "furthermore" is natural; 4-5 hedge/transition/recap phrases in a 500-word section is a fingerprint. Flag clusters, not lone uses.

1. **Hedging stacks** — "It's important to note that...", "It's worth considering that...", "Ultimately, it depends...", "It is essential to recognize...", "While X has its merits, Y also offers...". Flag when hedging adds no precision.
2. **Summarize-and-recap openings/closings** — "In conclusion...", "In summary...", "Overall...", section-end recaps; "Conclusion" sections that wrap with a neat bow. Also mid-essay recaps.
3. **Moralizing / didactic closings** — calls to collective action and responsibility framing: "it's essential for parents, educators, and policymakers to work collaboratively..."; safety/controversy disclaimers addressed to imagined readers.
4. **Generic examples** — placeholder illustrations with no specifics: "for example, a company might...", "consider a hypothetical scenario where...", "such as in the case of a typical organization".
5. **Listmania** — over-reliance on numbered/bulleted lists where prose would carry the argument; every point becomes a list; bullet lists whose items are themselves formulaic.
6. **Forced symmetry / balance** — "On one hand... on the other hand..." for every argument; excessive both-sides framing; "not just X, but also Y" / "Not X, but Y" / "X rather than Y" as a reflexive sentence shape.
7. **Rule-of-three adjective/phrase triples** — "rich, vibrant, and profound"; "adjective, adjective, and adjective"; "phrase, phrase, and phrase" as a default rhythm.
8. **Significance/legacy inflation** — "stands as / serves as a testament", "a vital/crucial/pivotal role", "underscores its importance", "setting the stage for", "key turning point", "evolving landscape", "indelible mark", "deeply rooted", "plays a crucial role in shaping".
9. **Flat affect / "Wikipedia voice"** — grammatically perfect but emotionally flat; vague abstractions instead of concrete detail; avoidance of copulatives ("serves as / stands as / represents / boasts / features / offers" instead of "is").
10. **Elegant variation / synonym proliferation** — repetition-penalty artifact: avoiding reusing a word, so synonyms multiply unnecessarily.
11. **Promotional/ad-like language** — "boasts a", "vibrant", "rich", "profound", "enhancing", "showcasing", "exemplifies", "nestled", "in the heart of", "groundbreaking", "renowned".
12. **Formatting tells** (flag lightly — only when they harm clarity) — em-dash overuse (signal, not proof); inline-header vertical lists everywhere; mechanical boldface of every key term; thematic breaks before every heading.

**Sources:** Wikipedia, *Signs of AI writing*; Leap AI, *Hedging Words in AI Text*; WriteHuman, *The Real Signature of AI Writing* (2026 frequency data); Riedman Report, *How to spot AI writing with 10 easy tells*; Pinker, *The Sense of Style*.

---

## 6. Punctuation & mechanics (light — only clarity-harming cases)  [CANONICAL]

The skill does NOT copy-edit, so flag only the few mechanical errors that harm clarity. All have canonical fixes the author can verify against.

1. **Comma splice** — two independent clauses joined by only a comma: "The build passed all tests, we deployed to production." (needs period / semicolon / comma+FANBOYS / subordination).
2. **Run-on / fused sentence** — two complete sentences with no punctuation: "The build passed all tests we deployed to production."
3. **Comma before a conjunctive adverb (the "however splice")** — "The tests passed, however we rolled back." Needs a semicolon or period. Common and easily missed.
4. **Ambiguous pronoun reference** — orphan "this" with no noun ("This is why users see stale data." → "This combination of stale caches..."); ambiguous "it/they" with two possible antecedents; vague "which" pointing at a whole clause. Diagnostic: never let "this" stand alone — give it a noun.
5. **Excessive em-dashes** [CRAFT signal] — em-dash density as an AI/casual-writing tell (18.5% of AI inputs vs 7.1% humanized in 2026 data). Flag density, not individual uses.
6. **Sentence fragments** [CANONICAL] — "Although the sample size was limited." with no main clause.

**Out of scope (pure mechanics — do NOT flag):** serial commas, possessive 's, parenthetic comma placement, hyphenation style. Restrict to the clarity-harming subset above.

**Sources:** datafield.dev, *Chapter 6*; University of Utah Writing Center, *Run-Ons and Comma Splices*; Strunk, *Elements of Style* II; Methodist University Writing Center, *The Dirty Dozen*; WriteHuman, em-dash frequency data.

---

## Consolidated sources

- Strunk, *Elements of Style* — https://en.wikisource.org/wiki/The_Elements_of_Style/Rules — https://en.wikisource.org/wiki/The_Elements_of_Style/Misuse
- Orwell, *Politics and the English Language* — https://www.orwellfoundation.com/the-orwell-foundation/orwell/essays-and-other-works/politics-and-the-english-language/
- Williams, *Style: Toward Clarity and Grace* — https://www.michbar.org/file/generalinfo/plainenglish/pdfs/92_jan.pdf
- Pinker, *The Sense of Style* — https://www.psychologicalscience.org/observer/the-curse-of-knowledge-pinker-describes-a-key-cause-of-bad-writing
- Zinsser, *On Writing Well* (clutter) — https://www.litcharts.com/lit/on-writing-well/chapter-3-clutter
- datafield.dev, *Chapter 6: Sentences That Work* — https://datafield.dev/technical-writing/part-02/chapter-06/
- Trinka.ai, *20 Common Mistakes Non-Native Speakers* — https://www.trinka.ai/blog/the-20-most-common-grammar-mistakes-made-by-non-native-english-speakers/
- Editor World, *Common Mistakes Non-Native Speakers* — https://www.editorworld.com/article/common-english-mistakes-non-native-speakers
- Collins, *Common Errors in English* (PDF) — https://languageadvisor.net/wp-content/uploads/2022/01/Collins-Common-Errors-in-English.pdf
- Merriam-Webster, *5 Verbal Slip Ups* — https://www.merriam-webster.com/grammar/mondegreens-eggcorns-malapropisms-spoonerism-freudian-slip
- Grammarly, *Best Eggcorn Examples* — https://www.grammarly.com/blog/grammar/best-eggcorn-examples/
- MLA Style Center, *Malaprops and Near Misses* — https://style.mla.org/malaprops-and-other-near-misses/
- Daily Writing Tips, *50 Redundant Phrases* — https://www.dailywritingtips.com/50-redundant-phrases-to-avoid/
- Wikipedia, *Signs of AI writing* — https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
- WriteHuman, *Real Signature of AI Writing (2026)* — https://writehuman.ai/blog/ai-tells-in-2026
- Leap AI, *Hedging Words in AI Text* — https://www.tryleap.ai/learn/hedging-words-in-ai-text
- Riedman Report, *10 easy AI tells* — https://riedmanreport.substack.com/p/how-to-spot-ai-writing-with-10-easy
- University of Utah Writing Center, *Run-Ons and Comma Splices* — https://writingcenter.utah.edu/writing-resources/run-ons.php
- Methodist University, *The Dirty Dozen* (PDF) — https://www.methodist.edu/wp-content/uploads/2022/06/wc_handouts_dd.pdf