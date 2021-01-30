class quiz():
    def ask(qn):
        out = qn[]
    def __init__(self, name, jid):
        self.qns=[
            {
                'q': "Epistemology is the branch of Philosophy concerned with:",
                'opts': ['The meaninglessness of life', 'The nature of Being', '1The nature of knowledge and its sources', 'The nature, scope, and meaning of moral judgments'],
                'ans': "Epistemology is the branch of philosophy concerned with knowledge. Epistemologists study the nature of knowledge, epistemic justification, the rationality of belief, and various related issues. Epistemology is considered one of the four main branches of philosophy, along with ethics, logic, and metaphysics.\nby Wikipedia",
                'lv': 0,
                'topic': ['Epistemology', 'Base'],
                'answered': 0
            },
            {
                'q': "The distinction between a-priori and a-posteriori judgments is:",
                'opts': ['a meta-ethical one', 'an ontological one', '1an epistemological one', 'a matter of linguistic confusion'],
                'ans': "",
                'lv': 1,
                'topic': ['Epistemology', 'Kant'],
                'answered': 'no',
                'attempts': 0
            },
            {
                'q': "Which of the following is not a considered pragmatist Philosopher?:",
                'opts': ['Charles Sanders Peirce', 'William James', '1Gottlob Frege', 'John Dewey','Richard Rorty'],
                'ans': "",
                'lv': 1,
                'topic': '', 
                'answered': 'no',
                'attempts': 0
            }
        ]
        self.name = name
        self.jid = jid


