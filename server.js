

const express = require('express'); //Importera Express.js
const bodyParser = require('body-parser'); //Parse inkommande JSON data
const cors = require('cors'); //Tillåter frontend tex react på andra domän att kommunicera med servern
const {exec} = require('child_process');

const app = express(); //Tillverka en express application som hanterar http förfrågningar
const PORT = 3000; //Porten för backend

//Middleware 
app.use(cors()); //För frontend appar att skicka förfrågningar till backend
app.use(bodyParser.json()); //Tolka tex data som skickas från användare

//Test-rutt
app.get('/', (req, res) =>{
    res.send('Backend is running for GymTool!')

});

//Postrutten för träningsdatan
app.post('/data', (req, res) => {
    //För debug
    console.log("POST /data hit");
    const { sleep_hours, calories, emotional_state, gym_performance_scale, dates } = req.body;

    //Skapa JSONdata för att skicka till python
    const input = JSON.stringify({ sleep_hours, calories, emotional_state, gym_performance_scale, dates });

    //Debug
    console.log("JSON som skickas till Python:", input);

    //Kör python-scriptet
    exec(`python gymdata.py "${input.replace(/"/g, '\\"')}"`, (error, stdout, stderr) => {
        console.log("Python stdout:", stdout);
        console.log("Python stderr:", stderr);
    
        if (error) {
            console.error("Error: ${stderr}");
            res.status(500).send("Error: Ett fel uppstod vid krning av Python-skriptet");
            return;
        }
    
        try {
            const results = JSON.parse(stdout.trim());
            res.send(results);
        } catch (parseError) {
            console.error("Fel vid parsning av JSON frn Python:", parseError);
            res.status(500).send("Error: JSON frn Python kunde inte parsas");
        }
    });
});

//Startar servern och lyssnar efter inkommande förfrågningar 
app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});





