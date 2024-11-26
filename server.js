const express = require('express'); //Importera Express.js
const bodyParser = require('body-parser'); //Parse inkommande JSON data
const cors = require('cors'); //Tillåter frontend tex react på andra domän att kommunicera med servern

const app = express(); //Tillverka en express application som hanterar http förfrågningar
const PORT = 3000; //Porten för backend

//Middleware 
app.use(cors()); //För frontend appar att skicka förfrågningar till backend
app.use(bodyParser.json()); //Tolka tex data som skickas från användare

//Test-rutt
app.get('/', (req, res) =>{
    res.send('Backend is running for GymTool!')

});

//Startar servern och lyssnar efter inkommande förfrågningar 
app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});



