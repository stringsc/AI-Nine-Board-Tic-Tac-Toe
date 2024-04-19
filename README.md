Nine-Board Tic-Tac-Toe AI Agent

Overview
This project is part of the COMP3411 Artificial Intelligence course at UNSW for Term 1, 2024. It features an AI agent designed to play Nine-Board Tic-Tac-Toe, a complex variation of the traditional Tic-Tac-Toe game. The game consists of a 3x3 grid of Tic-Tac-Toe boards, and the agent's goal is to strategically place symbols to align three in a row on any of the nine boards, considering the moves within the global and local boards are interdependent based on the last move made.

Project Description
The AI agent operates in a sophisticated environment where each move by a player dictates the board in which the next player can make their move. This constraint adds a layer of strategic depth to the traditional game. The initial move is randomly placed, and players alternate placing their symbols, with the game ending in a draw if no moves are possible.

The agent is implemented to handle various scenarios, including initiating the game, responding to the opponent's moves, and strategically planning its moves to win or force a draw. It engages through a server-client setup where the game logic is managed by a server and move decisions are communicated via network sockets.

Technologies Used
- Programming languages: Python, Java, C/C++
- Tools: Makefile for building C/C++ applications, Python interpreter for Python applications
- Communication: Network sockets for interacting with the game server

Setup and Running
Instructions are provided for setting up the development environment and running the agent against different types of opponents, showcasing the agent's ability to adapt to various gameplay strategies.

Learning Outcomes
- Implementing AI strategies in a complex, rule-based game environment
- Developing network-based applications to interact with a remote server
- Enhancing problem-solving skills by developing algorithms that handle dynamic game states

How to Run
Detailed instructions are included for compiling the source code, starting the game server, and running the AI agent to play the game, either against another automated agent or in a self-play scenario.

To play against a computer player, you need to open another terminal window (and cd to the src directory).
Type this into the first window:

./servt -p 12345 -x

The program randt simply chooses each move randomly among the available legal moves. The Python program agent.py behaves in exactly the same way. You can play against it by typing this into the second window:

python3 agent.py -p 12345

You can play against a somewhat more sophisticated player by typing this into the second window:

./lookt -p 12345
(If you are using a Mac, type ./lookt.mac instead of ./lookt)

To play two computer programs against each other, you may need to open three windows. For example, to play agent against lookt using port 54321, type as follows:
  window 1:  ./servt -p 54321
  window 2:  ./agent -p 54321
  window 3:  ./lookt -p 54321
(Whichever program connects first will play X; the other program will play O.)

You can alternatively use the shell script playt.sh, and provide the executables and port number as command-line arguments. Here are some examples:
./playt.sh ./agent ./lookt 12345
./playt.sh "java Agent" ./lookt 12346
./playt.sh "python3 agent.py" ./lookt 12347

The strength of lookt can be adjusted by specifying a maximum search depth (default value is 9; reasonable range is 1 to 18), e.g.
./playt.sh "python3 agent.py" "./lookt -d 6" 31415

