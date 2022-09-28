import React, { Component, useState } from "react";
import './login.scss';
import axios from 'axios';
import Cookies from "js-cookie";

export const Login = () => {
    const [name, setName] = useState("");
    const [password, setPassword] = useState("");
    const handleSubmit = async (evt) => {
        if (evt) {
            evt.preventDefault();
        }
        const data = {
            email: name,
            password: password,
        };
        const news = async () => {
            let res = await axios
                .post("http://127.0.0.1:8000/login", data)
                .then((response) => {
                    console.log(response);
                    Cookies.set("token", response.data.access_token);
                    return response;
                })
                .catch((error) => {
                    console.log(error.message);
                });
            return res;
        };
        let x = await news();
        if (x) {
            window.location.reload();
        }
    };
    return (
        <>
            <div className="sectionLogin" >
                <div className="titleMain">
                    <h1>Connectez-vous</h1>
                    <h2>et Générez des mélodies uniques !</h2>
                </div>
                <form onSubmit={handleSubmit}>
                    <label>
                        <input
                            type="text"
                            className="email textInput"
                            placeholder="email"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                        ></input>
                    </label>
                    <label>
                        <input
                            type="password"
                            className="password textInput"
                            placeholder="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        ></input>
                    </label>
                    <input className="Btn" type="submit" value="Connexion" />
                </form>
            </div>
        </>
    );
};

