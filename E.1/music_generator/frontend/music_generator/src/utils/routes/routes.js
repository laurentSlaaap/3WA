import { React, useContext } from "react";
import {
    Switch,
    Route,
    Redirect
} from "react-router-dom";

import { GenerateSong } from "../../features/Generate_song/Generate_song.component.js";
import { Login } from "../../features/login/login.js";
import { Register } from "../../features/register/register.js";
import { Melodies } from "../../features/melodies/melodies.js";

export const Routes = (props) => {
    const Auth = useContext(props.AuthApi);
    return (
        <Switch>
            <ProtectedLogin
                path="/register"
                auth={Auth.auth}
                component={Register}
            ></ProtectedLogin>
            <ProtectedLogin
                path="/login"
                auth={Auth.auth}
                component={Login}
            ></ProtectedLogin>
            <ProtectedRoute
                path="/melodies"
                auth={Auth.auth}
                component={Melodies}
            ></ProtectedRoute>
            <ProtectedRoute
                path="/"
                auth={Auth.auth}
                component={GenerateSong}
            ></ProtectedRoute>

        </Switch>
    );
};
const ProtectedRoute = ({ auth, component: Component, ...rest }) => {
    return (
        <Route
            {...rest}
            render={() => (auth ? <Component /> : <Redirect to="/Login" />)}
        />
    );
};
const ProtectedLogin = ({ auth, component: Component, ...rest }) => {
    return (
        <Route
            {...rest}
            render={() => (!auth ? <Component /> : <Redirect to="/" />)}
        />
    );
};