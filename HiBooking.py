import streamlit as st
import time

from openai import OpenAI

#Set OpenAI api & assistant ID
api_key = "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"
assistant_id = "asst_ErpNupkB9mW5AlM8jWJjMZWq"

st.markdown("""
<style>
.big-font {
    font-size:20px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.lil-font {
    font-size:15px !important;
}
</style>
""", unsafe_allow_html=True)



st.markdown('<p class="lil-font">V.1.0 Using Open Assistant - initial product research  19/01/25</p>', unsafe_allow_html=True)

# Set openAi client , assistant ai and assistant ai thread
@st.cache_resource
def load_openai_client_and_assistant():
    client          = OpenAI(api_key=api_key)
    my_assistant    = client.beta.assistants.retrieve(assistant_id)
    thread          = client.beta.threads.create()
    client.beta.threads.delete(thread.id)
    thread          = client.beta.threads.create()

    return client , my_assistant, thread

client,  my_assistant, assistant_thread = load_openai_client_and_assistant()

# check in loop  if assistant ai parse our request

def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run


# initiate assistant ai response
def get_assistant_response(user_input=""):
    print()

    message = client.beta.threads.messages.create(
        thread_id=assistant_thread.id,
        role="user",
        content=user_input,
    )

    run = client.beta.threads.runs.create(
        thread_id=assistant_thread.id,
        assistant_id=assistant_id,
    )

    run = wait_on_run(run, assistant_thread)

    # Retrieve all the messages added after our last user message
    messages = client.beta.threads.messages.list(
        thread_id=assistant_thread.id, order="desc"
    )

    user_message = messages.data[0].content[0].text.value

    n = []

    for thread_message in messages.data:
        # Iterate over the 'content' attribute of the ThreadMessage, which is a list
        for content_item in thread_message.content:
            # Assuming content_item is a MessageContentText object with a 'text' attribute
            # and that 'text' has a 'value' attribute, print it
            n.append([content_item.text.value, thread_message.role])


    return n


if 'user_input' not in st.session_state:
    st.session_state.user_input = ''

def submit():
    st.session_state.user_input = st.session_state.query
    st.session_state.query = ''


st.title("HiBooking")
st.markdown('<p class="big-font">The ultimate AI booking assistant</p>', unsafe_allow_html=True)
st.markdown('<p></p>', unsafe_allow_html=True)
st.markdown('<p></p>', unsafe_allow_html=True)



st.text_input("How can I help?", key='query', on_change=submit)


user_input = st.session_state.user_input

st.markdown(f":green-background[**You**: {user_input}]")


if user_input:
    result = get_assistant_response(user_input)



    
    count = 0
    
    for r in result:

        Content_message = r[0]

        if r[1] == "assistant":
            if count == 0:
                st.write(f":red-background[**Jono**: {Content_message}]")
            else:
                st.markdown(f":grey[**Jono**: {Content_message}]")

        else:
            if count == 1:
                st.header(' ', divider='grey')
            else:
                st.markdown(f"**You**: :blue[{Content_message}]")

        count +=1

