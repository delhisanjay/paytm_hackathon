
import face_recognition
import cv2
from twilio.rest import Client
from django.contrib.auth.models import User
from django.urls import reverse

from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from django.views.generic import TemplateView
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView

from home.models import Patient_Detail, Doctor_Profile


class Home(TemplateView):
    template_name = 'home.html'
    # model=Doctor_Profile
    # def post(self, request, *args, **kwargs):
    #     c = self.request.POST.get('form-name')
    #     l = Doctor_Profile.objects.filter(category=c)
    #     print(l)
    # def get(self, request, *args, **kwargs):
    #     patient = Patient_Detail.objects.filter(pk=2)
    #     return render(request, 'activity.html', {'p': patient})


class SignUp(TemplateView):
    template_name = 'signup.html'
    # model=Doctor_Profile
    # l=Doctor_Profile.objects.filter(city='New Delhi')
    # print(l)
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            first_name = self.request.POST.get('first_name')
            last_name = self.request.POST.get('last_name')
            email=self.request.POST.get('email')
            username = self.request.POST.get('username')
            password= self.request.POST.get('password')
            form = User.objects.create_user(first_name=first_name, last_name=last_name,email=email, username=username,password=password)  # = wala model ka naam
            form.save()
            return HttpResponseRedirect(reverse('user_login'))


# class LogIn(TemplateView):
#     template_name = 'login.html'

def user_login(request):
    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')


        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        ###########################################Face
        # Get a reference to webcam #0 (the default one)
        video_capture = cv2.VideoCapture(0)

        # Load a second sample picture and learn how to recognize it.
        biden_image = face_recognition.load_image_file("sanjay.jpg")
        biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

        # Load a sample picture and learn how to recognize it.
        obama_image = face_recognition.load_image_file("gourav.jpg")
        obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

        # Create arrays of known face encodings and their names
        known_face_encodings = [
            biden_face_encoding,
            obama_face_encoding
        ]
        known_face_names = [
            "sanjay",
            "Gourav"

        ]

        # Initialize some variables
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True
        faces = []

        while True:
            # Grab a single frame of video
            ret, frame = video_capture.read()

            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time
            if process_this_frame:
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"

                    # If a match was found in known_face_encodings, just use the first one.
                    if True in matches:
                        first_match_index = matches.index(True)
                        name = known_face_names[first_match_index]

                    face_names.append(name)

            process_this_frame = not process_this_frame

            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            # Display the resulting image
            cv2.imshow('Video', frame)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            try:
                if name == 'sanjay':
                    print(name)
                    break
            except Exception as exception:
                continue


        ################################################

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request, user)

                if user.groups.filter(name='Doctor'):
                    # Release handle to the webcam
                    video_capture.release()
                    cv2.destroyAllWindows()
                    return HttpResponseRedirect(reverse('doctor'))
                elif user.groups.filter(name='LabUser'):
                    return HttpResponseRedirect(reverse('patient_details'))
                else:
                    return HttpResponse('Hey Customer')
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'login.html', {})

@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse('home'))

class Patient_login(TemplateView):
    template_name = 'patient_login.html'


def patient_login(request):

    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')


        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request, user)

                if user.groups.filter(name='Doctor'):
                    return HttpResponseRedirect(reverse('doctor'))
                else:
                    return HttpResponseRedirect(reverse('activity'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'patient_login.html', {})
# @method_decorator(login_required, name='dispatch')
# class Patient_details(ListView):
#     model=Patient_Detail
#     template_name = 'patient-details.html'
#     # def get_queryset(self):
#     #     return Patient.objects.filter(provider=self.request.user).order_by('-id')
#     # def get_queryset(self):
#     #     return User.objects.filter(groups__name='Doctor')
#
    # def get(self, request, *args, **kwargs):
    #     features = User.objects.filter(groups__name='Doctor')
    #     patient = Patient_Detail.objects.all()
    #     hospital=Hospital.objects.all()
    #     return render(request, 'patient-details.html', {'f': features, 'p': patient, 'hospital':hospital})
#
@method_decorator(login_required, name='dispatch')
class activity(TemplateView):
    template_name = 'activity.html'
    model = Patient_Detail

    # b=Patient_Detail.objects.get(pk=2)
    # print(b)
    def get(self, request, *args, **kwargs):
        patient = Patient_Detail.objects.filter(pk=2)
        return render(request, 'activity.html', {'p': patient})


class Profile(ListView):
    template_name = 'profile.html'
    model= Patient_Detail
    # b=Patient_Detail.objects.get(pk=2)
    # print(b)
    def get(self, request, *args, **kwargs):
        patient = Patient_Detail.objects.filter(pk=1)
        return render(request, 'profile.html', {'p': patient})

@method_decorator(login_required, name='dispatch')
class Book(TemplateView):
    template_name = 'booking.html'

class BookNow(TemplateView):
    template_name = 'book-now.html'

def sms(request):
    account_sid = '#'
    auth_token = '#'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body='Your Appointment is booked',
        from_='whatsapp:+14155238886',
        to='whatsapp:+917206755167'
    )



class Doctor(TemplateView):
    template_name = 'doctor-dashboard.html'

