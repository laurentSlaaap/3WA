import React from "react";
import './header-component.scss';
import { Link } from "react-router-dom";

export const Header = (props) => {

    return (
        <>
            {props.auth ? (
                <div className="Header">
                    <div className="Header-title">
                        <h2>Music Generator</h2>
                        <span className="Header-credits">Laurent Callens</span>
                    </div>
                    <div className="nav">
                        <div className="nav__content">
                            <ul className="nav__list">
                                <Link to="/" className="nav__list-item">Accueil</Link>
                                <Link to="/melodies" className="nav__list-item">Mélodies générées</Link>
                                <button className="quitBtn nav__list-item" onClick={props.disconnect}>Deconnexion</button>
                            </ul>
                            
                        </div>
                    </div>
                </div>
            ) : (
                <div className="Header">
                    <div className="Header-title">
                        <h2>Music Generator</h2>
                    </div>
                    <div className="Header-credits">
                        <span>Laurent Callens</span>
                    </div>
                    <div className="nav">
                        <div className="nav__content">
                            <ul className="nav__list">
                                <Link to="/login" className="nav__list-item"> Connexion</Link>
                                <Link to="/" className="nav__list-item"> Accueil</Link>
                                <Link to="/register" className="nav__list-item"> Inscription</Link>
                            </ul>
                        </div>
                    </div>
                </div>
            )}
        </>
    )
}