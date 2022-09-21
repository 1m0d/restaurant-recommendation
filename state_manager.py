from transitions import Machine
# from https://github.com/pytransitions/transitions

#NOTE that you cannot immediately pass the dialog act into this.
#To call the right state trigger, you need to take into account the following:
#Inform is split into inform_known and inform_unknown, to account for people asking for keywords we don't know.
#Deny is split into deny and deny_w_info, so that when a deny function gets passed with a keyword, we can read it as a dislike (opposite of a preference).
#There is a trigger do_check_table which needs to be called when state check_table is entered.
    #Did not know how to code this last part, so it will need to be written into the code which calls on this state manager.
#ALSO NOTE that the functions at the end each have an argument other than self. IDK how this works implementation wise... maybe they should just be defined outside this class.
    
    
class StateManager(object):
    states = ['neutral', #0 - This should lead to maybe 2-3 variations in text responses:
                          #Such as repeating info about a recently recommended restaurant
                          #or asking again "how can I help you further?"
              'suggest_restaurant', #1
              'request_missing_info', #2
              'say_bye_exit', #3
              'return_requested_info', #4
              'youre_welcome', #5
              'greet', #6
              'suggest_to_replace', #7
              'repeat_statement', #8
              'suggest_other_keyword', #9
              'check_table'] #10 check table of slots to see if its full
    
    def __init__(self, name, text_zero):
        self.name = name
        self.last_text = text_zero
        self.machine = Machine(model=self, states=StateManager.states, initial='neutral')

        #self.machine.add_transition(trigger='', source='', dest='')
        
        #The following two lines are moot so far, but leaving them in, just in case we need to add a "before/after"
        self.machine.add_transition(trigger='negate', source='suggest_other_keyword', dest='neutral')
        self.machine.add_transition(trigger='negate', source='suggest_to_replace', dest='neutral')
        #The universal path for negate
        self.machine.add_transition(trigger='negate', source='*', dest='neutral')
        
        #The paths for ack and null are boring so far
        self.machine.add_transition(trigger='ack', source='*', dest='neutral')
        self.machine.add_transition(trigger='null', source='*', dest='neutral')
        
        #Restart will always lead you to the initial text again (minus the welcome), stating your options
        self.machine.add_transition(trigger='restart', source='*', dest='neutral', after='restate_options')
        
        #In the following cases, affirm should do something then lead to neutral
        self.machine.add_transition(trigger='affirm', source='suggest_to_replace', dest='check_table', before='override_slot')
        self.machine.add_transition(trigger='affirm', source='suggest_other_keyword', dest='check_table', before='update_slot')
        
        #In neutral/unknown cases, these will all repeat the most recent message (in similar or the same wording)
        self.machine.add_transition(trigger='repeat', source='*', dest='repeat_text')
        self.machine.add_transition(trigger='affirm', source='*', dest='repeat_text')
        
        #When inform keyword is known, add it to the slot table
        self.machine.add_transition(trigger='inform_known', source='*', dest='check_table', before='update_slot')
        
        #These are straightforward
        self.machine.add_transition(trigger='inform_unknown', source='*', dest='suggest_other_keyword')
        self.machine.add_transition(trigger='hello', source='*', dest='greet')
        self.machine.add_transition(trigger='bye', source='*', dest='say_bye_exit')
        self.machine.add_transition(trigger='reqalts', source='*', dest='suggest_to_replace')
        self.machine.add_transition(trigger='thankyou', source='*', dest='youre_welcome')

        #When deny is detected with some keyword, we label it as !thatkeyword, as a preference AGAINST
        self.machine.add_transition(trigger='deny', source='*', dest='neutral')
        self.machine.add_transition(trigger='deny_w_info', source='*', dest='check_table', before='override_slot')

        
        #For now, these do the same thing(like in most example cases)
        self.machine.add_transition(trigger='confirm', source='*', dest='return_requested_info')
        self.machine.add_transition(trigger='request', source='*', dest='return_requested_info')
        
        #CHANGE LATER: make sure it's either a new restaurant or note that there are no other restaurants
        self.machine.add_transition(trigger='reqmore', source='*', dest='suggest_restaurant')

        #This would need to be triggered by a non-dialog act
        self.machine.add_transition(trigger='do_check_table', source='check_table', dest='suggest_restaurant')


    def say_hello(self):
        print("Hello!")
        
    def say_goodbye(self):
        print("Thank you for using this restaurant recommendation system! Goodbye!")
        
    def repeat_text(self):
        print(self.last_text)
        
    def restate_options(self):
        print("SOME LINE INDICATING WHAT YOU CAN ASK THE MACHINE")
        
    #PROBLEM with the following three functions -- 
    #idk if in such a state manager how you'd pass arguments into functions. Maybe define outside class.
    def append_last_text(self, text):
        self.last_text = text
              
    def override_slot(self, keyword):
        return "add later"
        #This function should override the keyword currently in the respective slot
        #NOTE that if it came from a "deny_w_keyword" it should be read as anything BUT that keyword
        
    def update_slot(self, keyword):
        return "add later 2"
        #This function should add the keyword to the correct slot (could prob be merged with above function)