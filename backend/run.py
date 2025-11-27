from app import create_app
from app.services.data_service import data_service
from app.utils.logger import log_startup, log_shutdown, api_logger, log_error
import traceback

app = create_app()

if __name__ == '__main__':
    try:
        # Log startup
        log_startup()
        
        # Load data
        data_service.load_data()
        
        # Print startup banner
        print("\n" + "="*50)
        print("Zee Movie Recommender API")
        print("="*50)
        print("Running on: http://localhost:5000")
        print("Endpoints:")
        print("   GET  /api/health")
        print("   GET  /api/movies?search=<query>&limit=<n>")
        print("   GET  /api/trending?limit=<n>")
        print("   POST /api/recommend")
        print("   GET  /api/stats")
        print("="*50)
        print("Logs are being written to:")
        print("   - backend/logs/api.log")
        print("   - backend/logs/error.log")
        print("   - backend/logs/access.log")
        print("="*50 + "\n")
        
        api_logger.info("Starting Flask server on port 5000")
        
        # Run the app
        app.run(debug=True, port=5000, use_reloader=False)
        
    except KeyboardInterrupt:
        log_shutdown()
        api_logger.info("Server stopped by user")
    except Exception as e:
        log_error("Startup Error", str(e), traceback.format_exc())
        raise
