from flask import request,jsonify, Response
from celery.result import AsyncResult
from flask import request
from make_celery import flask_app,generate_csv
import os
import constants

@flask_app.route('/trigger_report', methods=['POST'])
def trigger_report():
    result=generate_csv.delay()
    return jsonify({'report_id': result.id})

@flask_app.route('/get_report', methods=['GET'])
def get_report():
    report_id = request.args.get('report_id')
    result = AsyncResult(report_id)
    print(result.ready())
    if result.ready():
        # Task has completed
        if result.successful():
            if result.successful():
                filename=result.result
                # Construct the full path to the file
                full_path = os.path.join(constants.upload_folder_output, filename)
                
                # Create a response with the file and additional data
                response = Response()
                response.headers['Content-Disposition'] = f'attachment; filename={filename}'
                response.data = open(full_path, 'rb').read()
                response.headers['Content-Type'] = 'application/octet-stream'  # Set appropriate content type
                # Add your additional data to the response
                response.headers['X-Custom-Header'] = 'Complete'
                return response            
        else:
            # Task completed with an error
            return jsonify({'status': 'ERROR', 'error_message': str(result.result)})
    else:
        # Task is still pending
        return jsonify({'status': 'Running'})

if __name__ == "__main__":
    flask_app.run(debug=True)