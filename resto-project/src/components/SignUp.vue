<template>
    <div class="register">
        <img class="app-logo" src="../assets/logo.png">
        <input type="text" placeholder="Username" class="input-field" />
        <input type="email" placeholder="Email" class="input-field" />
        <input type="password" placeholder="Password" class="input-field" />
        <button class="submit-btn">Sign Up</button>
    </div>
</template>

<script>
export default {
    name: 'SignUp'
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