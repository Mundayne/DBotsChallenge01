'use strict';

const FS = require('fs');
const phrases = JSON.parse(FS.readFileSync(__dirname + '/lero.json', 'latin1'));

module.exports = {
    name: 'lero',
    async run(Client, message, args) {
        let raffle = [];
        let quantity = 0;
        let filter = (m) => !isNaN(m.content);

        message.channel.send('How many sentences do you want? (max of 10)');
        let collector = message.channel.createMessageCollector(filter, { max: 1 });

        collector.on('collect', (msg) => {
            if (parseInt(msg.content) > 10) return message.channel.send('Maximum of 10 sentences.');
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

            // If the message exceeds the discord's maximum length
            if (reply.join('\n').length > 2000) {
                do {
                    // Remove one sentence from it
                    reply.splice(-1, 1);

                    // Until it's length is less then the discord's maximum length
                } while (reply.join('\n').length > 2000);
            }

            message.channel.send(reply.join('\n'));
        });
    },
};
