# Korean Teaching System Test Documentation
## Sentence Complexity Testcases
```
<test_case id="simple_1">
    <english_sentence>I eat rice</english_sentence>
    <vocabulary>
        <word>
            <english>I</english>
            <korean>나</korean>
            <transliteration>na</transliteration>
        </word>
        <word>
            <english>eat</english>
            <korean>먹다</korean>
            <transliteration>meokda</transliteration>
        </word>
        <word>
            <english>rice</english>
            <korean>밥</korean>
            <transliteration>bap</transliteration>
        </word>
    </vocabulary>
    <structure>[Subject] + [Object] + [Verb]</structure>
    <considerations>
        - Consider which particle marks the subject
        - Think about the correct particle for the object
        - The verb needs to be conjugated for politeness level
        - Present tense form shows habitual or current action
    </considerations>
    <expected_korean>나는 밥을 먹어요</expected_korean>
</test_case>

<test_case id="past_tense">
    <english_sentence>I went to school yesterday</english_sentence>
    <vocabulary>
        <word>
            <english>I</english>
            <korean>나</korean>
            <transliteration>na</transliteration>
        </word>
        <word>
            <english>go</english>
            <korean>가다</korean>
            <transliteration>gada</transliteration>
        </word>
        <word>
            <english>school</english>
            <korean>학교</korean>
            <transliteration>hakgyo</transliteration>
        </word>
        <word>
            <english>yesterday</english>
            <korean>어제</korean>
            <transliteration>eoje</transliteration>
        </word>
    </vocabulary>
    <structure>[Subject] + [Time] + [Location] + [Verb in past tense]</structure>
    <considerations>
        - Time expression typically comes early in Korean
        - Direction particle needed to show movement toward destination
        - Verb must show the action happened in the past
        - Past tense changes the verb stem ending
    </considerations>
    <expected_korean>나는 어제 학교에 갔어요</expected_korean>
</test_case>

<test_case id="question_form">
    <english_sentence>What is this?</english_sentence>
    <vocabulary>
        <word>
            <english>what</english>
            <korean>뭐</korean>
            <transliteration>mwo</transliteration>
        </word>
        <word>
            <english>this</english>
            <korean>이것</korean>
            <transliteration>igeot</transliteration>
        </word>
    </vocabulary>
    <structure>[Demonstrative] + [Question word] + [Polite question form]</structure>
    <considerations>
        - Demonstrative can be contracted in natural speech
        - Question word comes before the copula
        - Polite question ending is different from statement
        - Think about proximity - what does "this" indicate about distance
    </considerations>
    <expected_korean>이게 뭐예요?</expected_korean>
</test_case>

<test_case id="location_existence">
    <english_sentence>The book is on the table</english_sentence>
    <vocabulary>
        <word>
            <english>book</english>
            <korean>책</korean>
            <transliteration>chaek</transliteration>
        </word>
        <word>
            <english>table</english>
            <korean>테이블</korean>
            <transliteration>teibeul</transliteration>
        </word>
        <word>
            <english>on</english>
            <korean>위</korean>
            <transliteration>wi</transliteration>
        </word>
    </vocabulary>
    <structure>[Subject] + [Location] + [Existence verb]</structure>
    <considerations>
        - Existence verb shows something is located somewhere
        - Location relationship word needs specific particle
        - Subject particle marks what exists in the location
        - Think about how to express spatial relationships
    </considerations>
    <expected_korean>책이 테이블 위에 있어요</expected_korean>
</test_case>

<test_case id="desire_form">
    <english_sentence>I want to drink coffee</english_sentence>
    <vocabulary>
        <word>
            <english>I</english>
            <korean>나</korean>
            <transliteration>na</transliteration>
        </word>
        <word>
            <english>want</english>
            <korean>원하다</korean>
            <transliteration>wonhada</transliteration>
        </word>
        <word>
            <english>drink</english>
            <korean>마시다</korean>
            <transliteration>masida</transliteration>
        </word>
        <word>
            <english>coffee</english>
            <korean>커피</korean>
            <transliteration>keopi</transliteration>
        </word>
    </vocabulary>
    <structure>[Subject] + [Object] + [Verb in desire form]</structure>
    <considerations>
        - Desire is expressed by combining verb stem with specific ending
        - Object particle marks what you want to consume
        - The verb form changes completely from dictionary form
        - Think about how to connect wanting with the action verb
    </considerations>
    <expected_korean>나는 커피를 마시고 싶어요</expected_korean>
</test_case>

<test_case id="progressive_action">
    <english_sentence>She is studying Korean</english_sentence>
    <vocabulary>
        <word>
            <english>she</english>
            <korean>그녀</korean>
            <transliteration>geunyeo</transliteration>
        </word>
        <word>
            <english>study</english>
            <korean>공부하다</korean>
            <transliteration>gongbuhada</transliteration>
        </word>
        <word>
            <english>Korean</english>
            <korean>한국어</korean>
            <transliteration>hangugo</transliteration>
        </word>
    </vocabulary>
    <structure>[Subject] + [Object] + [Verb in progressive form]</structure>
    <considerations>
        - Progressive shows action happening right now
        - Different from simple present tense
        - Requires special verb construction
        - Think about ongoing vs completed action
    </considerations>
    <expected_korean>그녀는 한국어를 공부하고 있어요</expected_korean>
</test_case>

<test_case id="companion_action">
    <english_sentence>I watch movies with my friend</english_sentence>
    <vocabulary>
        <word>
            <english>I</english>
            <korean>나</korean>
            <transliteration>na</transliteration>
        </word>
        <word>
            <english>watch</english>
            <korean>보다</korean>
            <transliteration>boda</transliteration>
        </word>
        <word>
            <english>movie</english>
            <korean>영화</korean>
            <transliteration>yeonghwa</transliteration>
        </word>
        <word>
            <english>friend</english>
            <korean>친구</korean>
            <transliteration>chingu</transliteration>
        </word>
    </vocabulary>
    <structure>[Subject] + [Companion] + [Object] + [Verb]</structure>
    <considerations>
        - Companion particle shows doing action together with someone
        - Object particle marks what is being watched
        - Think about the difference between alone vs with others
        - Companion relationship needs specific particle
    </considerations>
    <expected_korean>나는 친구와 영화를 봐요</expected_korean>
</test_case>

<test_case id="negative_form">
    <english_sentence>I don't eat meat</english_sentence>
    <vocabulary>
        <word>
            <english>I</english>
            <korean>나</korean>
            <transliteration>na</transliteration>
        </word>
        <word>
            <english>eat</english>
            <korean>먹다</korean>
            <transliteration>meokda</transliteration>
        </word>
        <word>
            <english>meat</english>
            <korean>고기</korean>
            <transliteration>gogi</transliteration>
        </word>
        <word>
            <english>not</english>
            <korean>안</korean>
            <transliteration>an</transliteration>
        </word>
    </vocabulary>
    <structure>[Subject] + [Object] + [Negative] + [Verb]</structure>
    <considerations>
        - Negation can be expressed in different ways
        - Negative word placement is different from English
        - Object particle still needed even in negative sentences
        - Think about where to place the negation word
    </considerations>
    <expected_korean>나는 고기를 안 먹어요</expected_korean>
</test_case>

<test_case id="complex_time">
    <english_sentence>Every morning I drink coffee at home</english_sentence>
    <vocabulary>
        <word>
            <english>every</english>
            <korean>매일</korean>
            <transliteration>maeil</transliteration>
        </word>
        <word>
            <english>morning</english>
            <korean>아침</korean>
            <transliteration>achim</transliteration>
        </word>
        <word>
            <english>I</english>
            <korean>나</korean>
            <transliteration>na</transliteration>
        </word>
        <word>
            <english>drink</english>
            <korean>마시다</korean>
            <transliteration>masida</transliteration>
        </word>
        <word>
            <english>coffee</english>
            <korean>커피</korean>
            <transliteration>keopi</transliteration>
        </word>
        <word>
            <english>home</english>
            <korean>집</korean>
            <transliteration>jip</transliteration>
        </word>
    </vocabulary>
    <structure>[Time] + [Time] + [Subject] + [Location] + [Object] + [Verb]</structure>
    <considerations>
        - Multiple time expressions can work together
        - Location particle shows where action happens
        - Time expressions typically come early
        - Think about habitual vs one-time action
        - Consider how frequency and time period combine
    </considerations>
    <expected_korean>매일 아침에 나는 집에서 커피를 마셔요</expected_korean>
</test_case>

<test_case id="edge_case_honorific">
    <english_sentence>Teacher, where are you going?</english_sentence>
    <vocabulary>
        <word>
            <english>teacher</english>
            <korean>선생님</korean>
            <transliteration>seonsaengnim</transliteration>
        </word>
        <word>
            <english>where</english>
            <korean>어디</korean>
            <transliteration>eodi</transliteration>
        </word>
        <word>
            <english>go</english>
            <korean>가다</korean>
            <transliteration>gada</transliteration>
        </word>
    </vocabulary>
    <structure>[Vocative] + [Question word] + [Honorific verb form]</structure>
    <considerations>
        - Honorific speech required when addressing teacher
        - Vocative comma in English becomes different in Korean
        - Question word placement in Korean questions
        - Verb must be conjugated with respect form
        - Think about social relationship and appropriate speech level
    </considerations>
    <expected_korean>선생님, 어디에 가세요?</expected_korean>
</test_case>
```