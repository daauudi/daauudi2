from flask import Flask, Response
import json

app = Flask(__name__)

@app.route('/alkuluku/<int:luku>')
def alkuluku(luku):
    try:
        onko_alkuluku = True

        if luku < 2:
            onko_alkuluku = False
        else:
            jakaja = 2
            while jakaja < luku:
                if luku % jakaja == 0:
                    onko_alkuluku = False
                    break
                jakaja += 1

        vastaus = {
            "Number": luku,
            "isPrime": onko_alkuluku
        }

        return Response(
            response=json.dumps(vastaus),
            status=200
        )

    except Exception as e:
        return Response(
            response=json.dumps({"error": str(e)}),
            status=400
        )


if __name__ == '__main__':
    app.run(port=3000)