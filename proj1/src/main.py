import pygame
from model.State import State
from config import SCREEN_WIDTH, SCREEN_HEIGHT
import trace
import sys



def pygame_setup():
    pygame.init()
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Focus")
    return window

def start(window):
    state = State()
    
    running = True
    while running:
        state.run(window)
        if(state.get_state() == None):
            running = False

        pygame.display.flip()
    pygame.quit()

def main():
    window = pygame_setup()
    start(window)

# Create a Trace object
tracer = trace.Trace(
    ignoredirs=[sys.prefix, sys.exec_prefix],
    trace=0,
    count=1)

# Run the program and collect tracing data
tracer.run('main()')

# Create a report and write it to a file
r = tracer.results()
with open('trace_report.txt', 'w') as f:
    r.write_results(show_missing=True, coverdir=f)

if __name__ == "__main__":
    main()