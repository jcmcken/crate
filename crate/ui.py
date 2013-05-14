

def confirm(question, exit_on_no=True, exit_message='Exiting on user command'):
    while True:
        ans = raw_input(question + ' [y/N]: ')
        if ans == 'y':
            return True
        elif ans in ['n', 'N']:
            if exit_on_no:
                sys.stdout.write('%s\n' % exit_message)
                raise SystemExit
            else:
                return False
