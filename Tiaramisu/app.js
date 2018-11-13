'use strict';

// Require
const FS = require('fs');
const Discord = require('discord.js');
const { BOT_TOKEN } = require('dotenv').config().parsed;

const Client = new Discord.Client();
Client.Commands = new Discord.Collection();
Client.Prefix = '!';

// Get commands
FS.readdir('./Commands', (err, files) => {
    if (err) console.error(err);

    for (let file of files) {
        if (!file.includes('.js')) continue;

        let cmd = require(`./Commands/${file}`);

        Client.Commands.set(cmd.name, cmd);
    }
});

// Get events
FS.readdir('./Events', (err, files) => {
    if (err) console.error(err);

    for (let file of files) {
        if (!file.includes('.js')) continue;

        let evnt = require(`./Events/${file}`);

        Client.on(evnt.event, (...args) => evnt.run(Client, ...args));
    }
});

Client.login(BOT_TOKEN);