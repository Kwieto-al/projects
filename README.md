# Projects
Here is a series of coding projects and tasks over the years that I have attempted. Both complete and incomplete projects are on the repository. A summary below will detail the code, and will reflect on what could be improved.

## Messages — NEA for A-Level Computer Science (2019-2020)
As part of the Computer Science A-level, every student must complete an Individual coding project. I chose to do an end-to-end encrypted chat program for computers. 
The code is written mainly in Python, with SQL used inside the code.
There are two parts: the client side program, and the server side program. Chats were designed to allow multiple users to send and receive messages. When a message is sent, it is stored on the server database. All client side programs routinely check for new messages, and pull them from the server if so.
This project deepened my knowledge of SQL, and introduced me to sockets, salting inputs, and sending and receiving data over the internet.
Due to the pandemic, the project was never finished. As such, the chats are not encrypted. An idea to use SSH was unimplemented, and more complex features like file sharing, images etc. are unimplemented. 
As the code stands, it is a mess; packaging it all into a single class was a bad idea. The server must be set manually, and the code can break easily.
If in future a similar project is to be attempted, a more thorough, though out structure should be used.
