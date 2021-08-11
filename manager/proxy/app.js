const express = require("express");
const app = express();
const action = require("./routes/action");
const config = require("./config");
const cors = require("cors");

app.use("/action", action)
app.use(cors());

app.listen(config.port, () => {
    console.log(`Server Listening at http://localhost:${config.port}`)
});

