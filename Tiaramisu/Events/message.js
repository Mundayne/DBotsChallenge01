'use strict';

module.exports = {
    event: 'message',
    run(Client, message) {
        if (message.author.bot || !message.guild) return;

        let args = message.content.slice(Client.Prefix.length).trim().split(' ');
        let cmd = args.shift();

        if (Client.Commands.has(cmd)) {
            try {
                Client.Commands.get(cmd).run(Client, message, args);
            } catch (err) {
                message.channel.send('Something went wrong.');
                console.error(err);
            }
        }
    },
};
