import { React, Component, useState } from "react";
import './register.scss';
import axios from 'axios';

export const  Register = () => {

    const [firstname, setFirstName] = useState("");
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const handleSubmit = (evt) => {
        evt.preventDefault();

        const user = {
            "firstname": firstname,
            "lastname": name,
            "email": email,
            "password": password
        };
        axios
            .post("http://127.0.0.1:8000/register", user)
            .then((response) => {
                alert("compte crée");
                window.location =  ('/');
            })
            .catch((error) => {
                alert('Cet Email est déja utilisé');
            });
    };
    return (
        <div>
        <div className="sectionLogin">
            <div className="titleMain">
                <h1>Créez un compte</h1>
                <h2>Et créez des mélodies !</h2>
            </div>
            <form onSubmit={handleSubmit}>
                <label>
                    <input className="textInput" type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="email" />
                </label>
                <label>
                    <input className="textInput" type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="password" />
                </label>
                <input className="Btn" type="submit" value="Inscription" />
            </form>
        </div>
    </div>
    );
}


