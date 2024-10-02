from flask import Flask, request, jsonify
import ella  # Assuming you have your model in a file called ella.py
import hack  # Assuming you have some security monitoring

app = Flask(__name__)

# Define a route to handle API requests
@app.route('/ella', methods=['POST'])
def ella_response():
    try:
        # Extract the data from the POST request
        data = request.get_json()
        user_input = data.get('input')
        
        if user_input:
            ella_instance = ella.Ella()
            response = ella_instance.conversational_module.engage(user_input)
            return jsonify({"response": response})
        else:
            return jsonify({"error": "No input provided"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/hack', methods=['POST'])
def hack_monitoring():
    try:
        # Activate hack monitoring based on the request
        hack_instance = hack.Hack()
        # Start silent monitoring
        hack_instance.silent_monitor()
        return jsonify({"status": "Monitoring started"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)