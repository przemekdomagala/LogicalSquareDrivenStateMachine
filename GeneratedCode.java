// Interface representing a state
    public interface State {
        // Method to handle an event in the context
        void handleEvent(Context context);
    }

    public class s_and_z implements State {
    @Override
    public void handleEvent(Context context) {
        if (a == 2) {
            if (guardzik == False) {
                akszyn_reakszyn();
                context.setState(new g_and_2());
            }
        }
    }
}

public class g_and_2 implements State {
    @Override
    public void handleEvent(Context context) {
        if (z == 2) {
            if (no_akszyn == True) {
                context.setState(new z_and_2());
            }
        }
    }
}

public class z_and_2 implements State {
    @Override
    public void handleEvent(Context context) {
        if (palka_zapalka == "dwa_kije") {
            no_guard ();
            context.setState(new s_and_z());
        }
    }
}

public class Context {
        private State currentState;

        public Context() {
            // Setting initial state to the first state
            this.currentState = new s_and_z();
        }

        public void setState(State state) {
            this.currentState = state;
        }

        public void handleEvent() {
            // Delegating event handling to the current state
            this.currentState.handleEvent(this);
        }
    }

    public class Main {
        public static void main(String[] args) {
            Context context = new Context();
            for (int i = 0; i < 3; i++) {
                context.handleEvent();
            }
        }
    }