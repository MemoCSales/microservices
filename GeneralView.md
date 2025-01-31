# General view of the project
## Example of Team Division

| Microservice | Frontend Responsibility |
|--------------|------------------------|
| Auth Service (OAuth 2.0 authentication with 42) | Login, Signup, Profile Management |
| User Service (Friends, Stats) | User Profile, Friends List UI |
| Game Service (Pong, Realtime Play) | Game Canvas, WebSockets UI |
| Matchmaking Service (Tournaments) | Tournament Brackets, Matching System |
| Notification Service (Messages, Invites) | Alerts, Friend Requests UI |

## How would the microservices communicate
* Each microservice will expose an API using REST/WebSockets
* Frontend components call these APIs asynchronously
* Since we need to have a `single-page application` Docker & Reverse Proxy will serve all microservices


## How would each microservice implement its own frontend
Since each team member will implement its own service, they could also develop their own frontend components.

The approach to combine all the `microfrontend components` into a `Single Page Application (SPA)` to keep modularity and indepdentence.

### Strategy:
- How it works:
	* Each microfrontend component is deployed as an independent service
- The reverse proxy serves the correct frontend base on the URL path
	- /auth -> Auth Service Frontend
	- /game -> Game Service Frontend
	- /matchmaking -> Matchmaking Service Frontend
	- /tournament -> Tournament Service Frontend

#### Project Structure:
Example of project Structure without frontend implementation by each service (monolith arquitecture):
```bash
transcendance/
├── backend/                # Backend code
│   ├── manage.py           # Django entry point
│   ├── requirements.txt    # Python dependencies
│   ├── Dockerfile          # Backend-specific Dockerfile
│   ├── transcendance/      # Django project folder
│   │   ├── settings.py     # Django settings
│   │   ├── urls.py         # URL routing
│   │   └── ...
│   └── app/                # Your main application (custom logic)
│       ├── models.py       # Database models
│       ├── views.py        # Views logic
│       ├── urls.py         # App-specific routes
│       └── ...
├── frontend/               # Frontend code
│   ├── index.html          # Main HTML file
│   ├── style.css           # CSS file
│   ├── app.js              # Main JavaScript file
│   └── assets/             # Static assets like images/icons
├── docker-compose.yml      # Docker Compose file
├── README.md               # Documentation
└── .env                    # Environment variables (e.g., database credentials)
```

Example of project structure with frontend implementation by each service (microservice arquitecture):
```bash
/transcendence
 ├── /frontend-auth        # Auth Microfrontend (Bootstrap + Vanilla JS)
 ├── /frontend-game        # Game Microfrontend (Bootstrap + Vanilla JS)
 ├── /frontend-matchmaking # Matchmaking Microfrontend
 ├── /backend-auth         # Auth Backend Service (Django)
 ├── /backend-game         # Game Backend Service (Django)
 ├── /backend-matchmaking  # Matchmaking Backend Service (Django)
 ├── /nginx                # Nginx Reverse Proxy Config
 │   ├── Dockerfile
 │   ├── nginx.conf
 ├── docker-compose.yml    # Docker Compose to orchestrate services

```

#### Configure Nginx Reverse Proxy
- Create and configure a nginx.conf file in order to know each service location in our web app:
 
 #### Create the Nginx Dockerfile

 #### Define the `docker-compose.yml`

 #### Access Services
 - Frontend Auth: `https://localhost/auth/`
 - Frontend Game: `https://localhost/game/`
 - Frontend Matchmaking: `https://localhost/matchmaking/`
 - API Auth: `https://localhost/api/auth`
 - API Game: `https://localhost/api/game`
 - API Matchmaking: `https://localhost/api/matchmaking`

 It will help us make our project scalar and modular while comply with subject requirements of `Single Page Application`. And it will be easy to deploy since we are using NGINX


 ### Advanced Stuff
 - Adding a Load Balancer NGINX 
	* Distributes traffic across multiple instances of a microservice.
	* Prevents overloading a single server.
	* Ensures high availability
	* Nginx will automatically balance traffic across multiple instances of each microservice.
 - Adding a API GateWay
	* It will act as an entry point for all requests
	* Manages authentication, rate limiting, and request routing
	* Protects microservices from direct exposure to the internet
	* Can handle catching and API versioning
	- Implementing Kong as a GateWay:
		* Its open source
		* Add it to the docker-compose.yml file as a new service
		* Configure kong routes in `kong/kong.yml`
		* Run it with docker-compose
- Adding a Service Mesh
	* Manage communication between microservices
	* Adds security (mTLS encryption, service discovery)
	* Handles retries, timeouts, and observability.
	* Implementing a Service Mesh such as Istio
		* Install Istio
		* Enable Istio on Your Services
		* Define Istio Traffic Routing
	
### Advanced Project Overview
```scss
                                      ┌───────────────────┐
                                      │    User Request   │
                                      └────────▲──────────┘
                                               │
                                      ┌────────▼────────┐
                                      │  Load Balancer  │  <-- (Nginx / HAProxy)
                                      └────────▲────────┘
                                               │
                                      ┌────────▼────────┐
                                      │   API Gateway   │  <-- (Kong / Traefik)
                                      └────────▲────────┘
                                               │
      ┌──────────────────────────────┬────────┴───────────┬───────────────────────────┐
      │                              │                    │                           │
┌─────▼─────┐                ┌───────▼───────┐     ┌───────▼────────┐       ┌────────▼──────┐
│ Auth       │                │ Game          │     │ Matchmaking    │       │ Tournament    │
│ Microserv. │                │ Microservice  │     │ Microservice   │       │ Microservice  │
└─────▲─────┘                └───────▲───────┘     └───────▲────────┘       └────────▲──────┘
      │                              │                    │                           │
      └─────────────► (Service Mesh for Internal Communication) ◄────────────────────┘

```



## Definitions
- `Reverse proxy`: A reverse proxy is a server that sits between clients (like your computer or phone) and other servers (like websites or applications). When you request something (like a webpage), the reverse proxy takes your request, forwards it to the right server, gets the response, and sends it back to you. It helps with things like security (hiding the real server), load balancing (spreading requests evenly), and caching (storing data to make things faster). It’s like a middleman that makes sure everything runs smoothly and safely.

- `mTLS encryption (Mutual Transport Layer Security)`: It's like a double safe handshake. It is a security protocol that secures both parties between a communication (client - server). Verifies each other before exchanging information.
	Here's how it works:

	- `Digital certificates`: Both the client and the server have digital certificates that act as unique identifiers.

	- `Mutual verification`: When they connect, both exchange and validate their certificates to ensure they are who they claim to be.

	- `Secure connection`: Once verified, the communication is encrypted so that no one else can read it

	* mTLS is used in situations where security is critical, such as in banking applications, cloud services, or internal enterprise systems.

- `Service Mesh`: A service mesh is a dedicated infrastructure layer that manages communication between services in a microservices architecture. It handles tasks like:

	- Service-to-service communication: Routing requests between services efficiently.

	- Observability: Collecting data about traffic, latency, and errors to help monitor and debug the system.

	- Security: Encrypting traffic (e.g., with mTLS) and enforcing access control policies.

	- Resilience: Implementing retries, timeouts, and failovers to make the system more robust.
