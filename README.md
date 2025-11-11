# DDoSDetection
Features of the detection module

FastAPI

Used for defining the HTTP API and exposing the prediction endpoint.
Asynchronous Processing
Using asyncio and ThreadPoolExecutor allows the API to handle numerous concurrent requests together without blocking.

Batch Processing

Instead of processing each prediction independently, the system collects incoming requests in batches via a queue, processing multiple requests at a time. This reduces the overhead of loading the model repeatedly and accelerates inference by processing multiple inputs in parallel using the batch API of the model.

Lazy Model Loading

The model, one-hot-encoder and scaler are loaded only when needed, thus there is no unnecessary memory consumption when the app starts. This also reduces the initial overhead for loading the application.

Error Handling

if an error occurs while the batch worker is processing predictions, it will capture the error and notify the requests (corresponding to "futures") waiting for a result.
By doing so, it ensures that the system doesn't crash or hang; instead, the pending requests are informed about the error, and the system remains stable despite the failure. 

Deployment

The Detection module was deployed on a Docker container, making it suitable for deployment in local environments as well as cloud-based setups and simplifying inter-component communication
