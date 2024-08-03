const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const mongoose = require('mongoose');


const app = express();
mongoose.connect("mongodb://localhost:27017/minicaloriesdb", { useNewUrlParser: true, useUnifiedTopology: true });

const Caloriesschema = mongoose.Schema({
    gender: String,
    age: Number,
    height: Number,
    weight: Number,
    duration: Number,
    heartbeat: Number,
    bodytemp: Number
});

const newuser = mongoose.model("users", Caloriesschema);

app.use(bodyParser.json());
app.use(cors({
    origin: 'http://localhost:3000',
    methods: 'GET,POST,PUT,DELETE',
    credentials: true,
}));
app.post('/calories', (req, res) => {
    const { predicted_calories } = req.body;
    console.log("Predicted calories received:", predicted_calories);
    res.status(200).json({ predicted_calories });

    // Send predicted calories to the React frontend
    // sendCaloriesToReact(predicted_calories);
});


  app.post('/display-calories', (req, res) => {
    const { predicted_calories } = req.body;
    console.log("Predicted calories received in React:", predicted_calories);
    res.sendStatus(200); 
  });
  

app.listen(3001, () => {
    console.log("Server started on port 3001");
});
