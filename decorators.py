"""
Decorator used to embellish the phase announcement
"""
def phase_announcement(phase):
    def wrapper_function(method):
        def wrapper(self):
            print(f"\n{'-'*15}{phase.upper()} PHASE{'-'*15}\n")
            method(self)
        return wrapper
    return wrapper_function
