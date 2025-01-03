require('dotenv').config({path: '../.env'});

const config ={
    server: process.env.SERVER_URL,
    auth_port: process.env.AUTH_PORT,
    executive_port: process.env.EXECUTIVE_PORT ,
    receptionist_port: process.env.RECEPTIONIST_PORT,
    manager_port: process.env.MANAGER_PORT,
    data_port: process.env.DATA_PORT,
}
config.auth_domain= `${config.server}:${config.auth_port}`;
config.executive_domain= `${config.server}:${config.executive_port}`;
config.receptionist_domain= `${config.server}:${config.receptionist_port}`;
config.manager_domain= `${config.server}:${config.manager_port}`;
config.data_domain= `${config.server}:${config.data_port}`;

module.exports = config;