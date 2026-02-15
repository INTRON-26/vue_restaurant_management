<template>
    <div class="register">
        <img class="app-logo" src="../assets/logo.png">
        <input type="text" v-model="name" placeholder="Name" class="input-field" />
        <input type="email" v-model="email" placeholder="Email" class="input-field" />
        <input type="password" v-model="password" placeholder="Password" class="input-field" />
        <button v-on:click="signUp" class="submit-btn">Sign Up</button>
    </div>
</template>

<script>
export default {
    name: 'SignUp',
    data() {
        return {
            name: '',
            email: '',
            password: ''
        }
    },
    methods: {
        signUp() {
            // save it as json in local storage
            const userData = {
                name: this.name,
                email: this.email,
                password: this.password
            }
            localStorage.setItem('userData', JSON.stringify(userData));
            console.log('Name:', this.name);
            console.log('Email:', this.email);
            console.log('Password:', this.password);
        }
    }
}
</script>
<style>
.register {
    margin-top: 50px;
}

.app-logo {
    width: 500px;
}

.input-field {
    width: 300px;
    height: 40px;
    padding-left: 20px;
    display: block;
    margin-bottom: 30px;
    margin-right: auto;
    margin-left: auto;
    border: 1px solid 225b48;
    border-radius: 4px;
}

.submit-btn {
    width: 320px;
    height: 40px;
    border: 1px solid #225b48;
    background: #225b48;
    color: #ffffff;
    cursor: pointer;
    border-radius: 4px;
    font-size: 16px;    
    transition: background 0.3s ease;
}

.submit-btn:hover {
    background: #ffffff;
    color: #225b48;
    border: 2px solid #225b48;
}
</style>