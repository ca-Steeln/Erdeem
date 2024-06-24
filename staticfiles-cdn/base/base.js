
$(document).ready(function() {
    const pageLoadIndicator = document.getElementById('pageload-indicator');
    let formIndicator = document.getElementById('form-indicator');


    // document.addEventListener('htmx:xhr:loadstart', (e)=>{
    //     $(pageLoadIndicator).addClass('htmx-request');
    // });

    document.addEventListener('htmx:afterSettle', (e)=>{
        $(pageLoadIndicator).removeClass('htmx-request');
    })

    document.addEventListener('htmx:onLoadError', (e)=>{
        $(pageLoadIndicator).removeClass('htmx-request');

    })

    document.addEventListener('htmx:confirm', (e)=>{

        if(e.target.tagName === 'FORM'){
            $(formIndicator).addClass('htmx-request');
        }else{
            $(pageLoadIndicator).addClass('htmx-request');
        }
    })

    document.addEventListener('htmx:responseError', (e)=>{
        $(formIndicator).removeClass('htmx-request');
        $(pageLoadIndicator).removeClass('htmx-request');
    })
})


// document.addEventListener('htmx:htmx:beforeCleanupElement', (e)=>{
//     console.log('htmx:beforeCleanupElement')
// })

// document.addEventListener('htmx:beforeOnLoad', (e)=>{
//     console.log('beforeOnLoad')
// })

// document.addEventListener('htmx:beforeProcessNode', (e)=>{
//     console.log('beforeProcessNode')
// })

// document.addEventListener('htmx:beforeRequest', (e)=>{
//     console.log('beforeRequest')
// })

// document.addEventListener('htmx:beforeSwap', (e)=>{
//     console.log('beforeSwap')
// })


// document.addEventListener('htmx:beforeTransition', (e)=>{
//     console.log('beforeTransition')
// })

// document.addEventListener('htmx:oobBeforeSwap', (e)=>{
//     console.log('oobBeforeSwap')
// })

// document.addEventListener('htmx:xhr:loadstart', (e)=>{
//     console.log('htmx:xhr:loadstart')
// })

// document.addEventListener('htmx:xhr:progress', (e)=>{
//     console.log('htmx:xhr:progress')
// })