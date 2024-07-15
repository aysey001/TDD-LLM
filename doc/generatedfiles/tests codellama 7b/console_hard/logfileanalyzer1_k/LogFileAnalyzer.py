class LogFileAnalyzer:
    def __init__(self, logfile):
        self.logfile = logfile
        self.log = self.read_log()
        self.filters = {}

    def read_log(self):
        # Read log file and return a dictionary with log data
        with open(self.logfile, "r") as f:
            log = f.read()
        log = log.split("\n")
        log = [line.split(" ") for line in log]
        log = {line[0]: {"IP address": line[0], "timestamp": line[1], "request method": line[2], "URL": line[3], "status code": line[4], "response time": line[5]} for line in log}
        return log

    def calculate_summary(self):
        # Calculate summary of log file data
        # Return a dictionary with summary data
        summary = {}
        summary["total requests"] = len(self.log)
        summary["common request methods"] = self.get_common_request_methods()
        summary["top 10 most requested URLs"] = self.get_most_requested_urls()
        summary["response time per status code"] = self.get_response_time_per_status_code()
        return summary

    def detect_errors(self):
        # Detect errors in log file data
        # Return a dictionary with error data
        errors = {}
        errors["error"] = "Not Implemented"
        errors["count"] = 0
        return errors

    def print_summary(self, summary, errors):
        # Print summary of log file data and error data
        print("Log File Summary:")
        print(f"Total requests: {summary['total requests']}")
        print(f"Common request methods: {summary['common request methods']}")
        print(f"Top 10 most requested URLs: {summary['top 10 most requested URLs']}")
        print(f"Response time per status code: {summary['response time per status code']}")
        print("Errors:")
        print(f"Error: {errors['error']}")
        print(f"Count: {errors['count']}")

    def get_common_request_methods(self):
        # Return a list of common request methods
        # E.g., ["GET", "POST", "PUT", "DELETE"]
        request_methods = [log["request method"] for log in self.log.values()]
        request_methods = list(set(request_methods))
        return request_methods

    def get_most_requested_urls(self):
        # Return a list of the top 10 most requested URLs
        # E.g., ["/api/users", "/api/products", "/api/orders"]
        urls = [log["URL"] for log in self.log.values()]
        urls = [url for url in urls if url != ""]
        urls = sorted(urls, key=urls.count, reverse=True)[:10]
        return urls

    def get_response_time_per_status_code(self):
        # Return a dictionary with response time per status code
        # E.g., {"200": 100, "400": 50, "500": 20}
        response_times = {log["status code"]: log["response time"] for log in self.log.values()}
        response_times = {k: v for k, v in sorted(response_times.items(), key=lambda item: item[1])}
        return response_times