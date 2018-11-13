'use strict';

const FS = require('fs');
const phrases = JSON.parse(FS.readFileSync(__dirname + '/lero.json', 'latin1'));

module.exports = {
    name: 'lero',
    async run(Client, message, args) {
        let raffle = [];
        let quantity = 0;
        let filter = (m) => !isNaN(m.content);

        message.channel.send('How many sentences do you want? (max of 20)');
        let collector = message.channel.createMessageCollector(filter, { max: 1 });

        collector.on('collect', (msg) => {
            if (parseInt(msg.content) > 20) return message.channel.send('Maximum of 20 sentences.');
            if (parseInt(msg.content) < 1) return message.channel.send('Minimum of 1 sentence.');

            quantity = parseInt(msg.content);

            let reply = [];

            for (let i = 0; i < quantity; i++) {
                // A random number between 0 ~ 29
                raffle[0] = (Math.floor(Math.random() * 29));
                raffle[1] = (Math.floor(Math.random() * 29));
                raffle[2] = (Math.floor(Math.random() * 29));
                raffle[3] = (Math.floor(Math.random() * 29));

                reply.push(`${phrases['body0'][raffle[0]]} ${phrases['body1'][raffle[1]]} ${phrases['body2'][raffle[2]]} ${phrases['body3'][raffle[3]]}`);
            }

            message.channel.send(reply.join('\n'));
        });
    },
};
