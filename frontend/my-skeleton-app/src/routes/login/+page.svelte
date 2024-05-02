<script lang="ts">

    let email = '';
    let password = '';
    let brPokusaja = 0;
    import { AppShell, initializeStores } from '@skeletonlabs/skeleton';
    initializeStores();
    import { goto } from '$app/navigation';
    import { getToastStore } from '@skeletonlabs/skeleton';
    import { Toast, type ToastSettings, type ToastStore } from '@skeletonlabs/skeleton';
    import {userID} from '$lib/stores.js';
    import { onMount,onDestroy } from 'svelte';
    
    let isLoggedIn : String | null;
    onMount(()=> isLoggedIn = localStorage.getItem('isLoggedIn'))

    console.log('pokrenutaProvera');

    const toastStore = getToastStore();
    const validateEmail = (emailAdresa:String) => {
        return emailAdresa.match(
            /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
        );
    };

    async function submitFormLogin() {
        
        // @ts-ignore
        document.getElementById('email').setAttribute("required","true");
        // @ts-ignore
        document.getElementById('password').setAttribute("required","true");
        
        const formData = {
            email,
            password
        };

        if(validateEmail(email))
        {
            try {
                
                const response = await fetch('http://localhost:5000/login', {
                    method: 'POST',
                    credentials: 'include',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData)
                });

                const data = await response.json();
                console.log(data); // Handle response from backend
                if(data['message']==='Login successful')
                {
                    const t: ToastSettings = {
                        message: data['message'],
                        timeout:2000,
                        background:'bg-primary-600',
                        hideDismiss: true,
                    };
                    brPokusaja = 0;
                    toastStore.trigger(t);
                    setTimeout(() => {
                        if (data['message'] === 'Login successful') 
                        {
                            goto('/');
                            }
                        }, 2500);

                }
                else
                {
                    brPokusaja += 1;
                    const t: ToastSettings = {
                        message: data['message'],
                        timeout:2000,
                        background: 'bg-error-700',
                        hideDismiss: true,
                    };
                    toastStore.trigger(t);
                    if(brPokusaja>=3)
                    {
                        brPokusaja = 0;
                        setTimeout(() => {
                            goto('/register');
                                
                            }, 1500);
                    }
                }
                
            } catch (error) {
                console.error('Error:', error);
            }
        }
        else
        {
            const t: ToastSettings = {
                message: 'Unesi ispravan mail!',
                timeout:2000,
                background: 'bg-error-700',
                hideDismiss: true,
            };
            toastStore.trigger(t);
        }
    }
</script>

{#if isLoggedIn === 'false'}
    <nav class="btn-group variant-ghost-secondary [&>*+*]:border-red-500">
        <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/login">Login</a></li>
            <li><a href="/register">Register</a></li>
        </ul>
    </nav>


    <div style="display: flex; justify-content:center;">
        <form on:submit={submitFormLogin} class="text-surface-300" style="display:flex;justify-content:center;flex-direction:column;padding: 3rem;">
            <h1 class="h1">Please Log In.</h1>
            <label for="email" class="selfc h3">Email:</label>
            <input type="email" id="email" class="selfc input variant-form-material" placeholder="Unesi email:" bind:value={email}/>

            <label for="password" class="selfc h3" >Password:</label>
            <input type="password" id="password" class="selfc input variant-form-material" placeholder="Unesi sifru:" bind:value={password}/>

            <button id="loginDugme" type="submit" class="selfc btn variant-filled">Login</button>
        </form>
    </div>

{:else}
    <div style="display: flex; justify-content:center; flex-direction:column">
        <h1>VEC SI ULOGOVAN, VRATI SE NA POCETNU</h1>
        <li><a href="/">Home</a></li>
    </div>
{/if}
<Toast></Toast>

<style>
    *
    {
        text-align: center;
        display: block;
        margin: 2px;
        align-items: center;
        min-height: 50%;
    }
    :global(body)
    {
        height: 100vh;
        background: linear-gradient(to right, #1b5780, #504c52);
    }
    nav
    {
        display: flex;
        justify-content: end;
        padding: 10px;
        border-radius: 0%;
        position: sticky;
        height:fit-content;
        min-height: 0%;
    }
    ul
    {
        display:flex;
        align-items: flex-end;
        justify-content: end;
    }
    li
    {
        display: inline;
    }

    a
    {
        color:black;
        text-decoration: none;
        font-weight: bold;
    }
    .selfc
    {
        align-self:center;
    }
    button
    {
        background-color: lightblue;
    }
    #loginDugme
    {
        margin-top: 5%;
    }
</style>