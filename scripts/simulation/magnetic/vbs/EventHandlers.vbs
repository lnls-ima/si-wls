' ===================================================================
'
' This is a template user event handlers file with default handlers.
'
' To add your own custom code to customize the application's
' behavior:
'
' 1. Copy or rename this file to be EventHandlers.vbs. This will
'    cause the application to automatically load it at program
'    startup.
' 2. Uncomment out the applicable subroutines and add your own code.
'    All handler subroutines are commented out by default.
'
' Refer to the on-line help for a more in-depth explanation of the
' event handlers subroutines.
'
' Unpublished work. Copyright Siemens 2020.
'
' ===================================================================
Option Explicit

const PI= 3.14159265358979323846264338327950288419716939937510582097494459
Dim QUOTE
QUOTE= Chr(34)

' ========================================================
' Set the locale to US-English to ensure common processing
' of the number decimal point (.).
' ========================================================
Call SetLocale("en-us")

' =====================================================
' This is called once after the application is started.
' =====================================================
'Sub Application_OnLoad()
	'LNLS Plugins Start'
	'================================================================================================='
	Const sMacroMenuName = "LNLS" 
	Dim menubar, macromenu, command, dirpath
	Set menubar = getMenubar()
	Set macromenu = menubar.insertMenu("&Help", sMacroMenuName)

	command = "runScript(" & Chr(34) & "C:\Program Files\Siemens\Simcenter MAGNET 2021.2\LNLS_plugins\draw_shape.vbs" & Chr(34) & ")" 
	macromenu.appendItem "Draw Shape", command

	command = "runScript(" & Chr(34) & "C:\Program Files\Siemens\Simcenter MAGNET 2021.2\LNLS_plugins\vertex_parametrization.vbs" & Chr(34) & ")" 
	macromenu.appendItem "Vertex Parametrization", command

	command = "runScript(" & Chr(34) & "C:\Program Files\Siemens\Simcenter MAGNET 2021.2\LNLS_plugins\field_sampler.vbs" & Chr(34) & ")"
	macromenu.appendItem "Field Sampler", command

	command = "runScript(" & Chr(34) & "C:\Program Files\Siemens\Simcenter MAGNET 2021.2\LNLS_plugins\field_multipoles.vbs" & Chr(34) & ")"
	macromenu.appendItem "Field Multipoles", command

	command = "runScript(" & Chr(34) & "C:\Program Files\Siemens\Simcenter MAGNET 2021.2\LNLS_plugins\field_integrals.vbs" & Chr(34) & ")"
	macromenu.appendItem "Field Integrals", command

	command = "runScript(" & Chr(34) & "C:\Program Files\Siemens\Simcenter MAGNET 2021.2\LNLS_plugins\coil_resistance.vbs" & Chr(34) & ")"
	macromenu.appendItem "Coil Resistance", command

	command = "runScript(" & Chr(34) & "C:\Program Files\Siemens\Simcenter MAGNET 2021.2\LNLS_plugins\particle_trajectory.vbs" & Chr(34) & ")"
	macromenu.appendItem "Particle Trajectory", command

	command = "runScript(" & Chr(34) & "C:\Program Files\Siemens\Simcenter MAGNET 2021.2\LNLS_plugins\kick_map.vbs" & Chr(34) & ")"
	macromenu.appendItem "Kick Map", command

	command = "runScript(" & Chr(34) & "C:\Program Files\Siemens\Simcenter MAGNET 2021.2\LNLS_plugins\loadline_margin.vbs" & Chr(34) & ")"
	macromenu.appendItem "Load Line Margin", command
	'================================================================================================='
	'LNLS Plugins End'
	
	
	
	
	
'End Sub

' =====================================================
' This is called before when the application is closed.
' =====================================================
'Sub Application_OnUnLoad()
'End Sub

' ====================================================================
' This is called before each action that the application executes.
' Some commands are never parsed. In those cases, use the
' Application_OnLogCommand() instead since that is always called.
' Command: Contains the scripting code being executed.
'          It can be changed by the scripting code to modify behavior.
'          The modified command will be written to the session log and
'          passed to Application_OnLogCommand().
' ==================================================================== 
'Sub Application_OnParseCommand(Command)
'End Sub

' ===================================================================
' This is called after a command is parsed and executed.
' For commands that aren't parsed (rare case) this event might not be
' fired after the command is executed internally in the application.
' Command: Contains the equivalent scripting code.
' ===================================================================
'Sub Application_OnLogCommand(Command)
'End Sub

' ================================================================
' This is called for each message box dialog that is displayed.
' Message: The text being displayed in the dialog.
' BoxType: The type of message box. Refer to the documentation
'          of MsgBox() for more details.
' Answer:  The user's response.
'          When the UI is visible, this is called after the user
'          has answered and the event handler's Answer is ignored.
'          If the UI is invisible, then the event handler can
'          supply an answer. The default is OK. Refer to the
'          documentation of MsgBox() for more details.
' ================================================================
'Sub Application_OnMessageBox(Message, BoxType, Answer)
'End Sub

' ========================================================================
' This is called when the raiseUserEvent() scripting API is called.
' Data:     The variant data passed to raiseUserEvent(). It can be changed
'           to pass other data back to the caller.
' Category: The event handler category string passed to raiseUserEvent().
'           This is typically used to allow event handlers to only process
'           their own raised events.
' ========================================================================
'Sub Application_OnRaiseUserEvent(Data, Category)
'End Sub

' ========================================================================
' Called to notify event handlers that a new event handler is being added.
' Filepath: A string containing the path to the event handler file.
' Category: The category string of the new event handler.
' ========================================================================
'Sub Application_OnLoadEventHandlers(Filepath, Category)
'End Sub

' =======================================================================
' Called to notify event handlers that an event handler is being removed.
' Category: The category string of the event handler being removed.
' =======================================================================
'Sub Application_OnUnLoadEventHandlers(Category)
'End Sub

' =======================================================================
' Called whenever an unexpected exception is caught by the application.
' This event will be followed by a Application_OnMessageBox event.
' Exception: Contains the text that will be displayed in the message box.
' =======================================================================
'Sub Application_OnException(Exception)
'End Sub

' ======================================================================
' Called when a document is created or opened.
' If getFilePath() returns an empty string, then this is a new document.
' Otherwise, it returns the path to the document's file.
' ======================================================================
'Sub Document_OnLoad()
'End Sub

' =================================
' Called when a document is closed.
' =================================
'Sub Document_OnUnLoad()
'End Sub

' =================================================
' Called before the solver is started.
' SolutionType: One of the solution type constants.
' Frame:        Either 2 or 3.
' =================================================
'Sub Document_OnPreSolve(SolutionType, Frame)
'End Sub

' ===============================================================================
' Called after the solver has finished.
' Report: The solver report text that is displayed (if it is non-empty).
'         A non empty report will also generate a Application_OnMessageBox event.
' ===============================================================================
'Sub Document_OnPostSolve(Report)
'End Sub

' =====================================================================================
' Called during solving to provide feedback on the solver's activity.
' If there was a Gui abort or stop, this is called afterwards so Action will be set.
' FeedbackType:         One of the feedback type constants.
' Value:                A double-precision number. Its meaning depends on FeedbackType.
'                       It is typically used as a progress indicator value.
' Step:                 One of the feedback step constants (start, middle, end).
' ElapsedTimeInSeconds: The elapsed time in seconds since the start of the solve.
' Action:               One of the feedback action constants (continue, stop, abort).
'                       When the UI is visible, changing this argument has no effect
'                       unless infoFeedbackOverrideGui is added to the constant.
'                       If the UI is invisible, then the event handler can change this
'                       argument to stop or abort the solver.
' =====================================================================================
'Sub Document_OnSolverFeedback(FeedbackType, Value, Step, ElapsedTimeInSeconds, Action)
'End Sub


' =====================================================================================
' Called during initial mesh generation (for viewing, not solving) to provide feedback
' on the mesher's activity.
' If there was a Gui abort or stop, this is called afterwards so Action will be set.
' FeedbackType:         One of the feedback type constants.
' Value:                A double-precision number. Its meaning depends on FeedbackType.
'                       It is typically used as a progress indicator value.
' Step:                 One of the feedback step constants (start, middle, end).
' ElapsedTimeInSeconds: The elapsed time in seconds since the start of the meshing.
' Action:               One of the feedback action constants (continue, stop, abort).
'                       When the UI is visible, changing this argument has no effect
'                       unless infoFeedbackOverrideGui is added to the constant.
'                       If the UI is invisible, then the event handler can change this
'                       argument to stop or abort the mesher.
' =====================================================================================
'Sub Document_OnMesherFeedback(FeedbackType, Value, Step, ElapsedTimeInSeconds, Action)
'End Sub

' ======================================================================================
' Called whenever text is added to the Text Output Bar.
' If there was a Gui abort or stop, this is called afterwards so Action will be set.
' FeedbackType: One of the feedback type constants.
' Module:       One of the feedback module constants (mesher, post-processor, solver).
' Message:      The text of the message being added.
' Action:       One of the feedback action constants (continue, stop, abort).
'               When the UI is visible, changing this argument has no effect
'               unless infoFeedbackOverrideGui is added to the constant.
'               If the UI is invisible, then the event handler can change this
'               argument to stop or abort the module that is running.
' ======================================================================================
'Sub Document_OnMessageFeedback(FeedbackType, Module, Message, Action)
'End Sub

' ==================================
' Called whenever a view is created.
' ==================================
'Sub View_OnLoad()
'End Sub

' =================================
' Called whenever a view is closed.
' =================================
'Sub View_OnUnLoad()
'End Sub

' ==================================================================================
' Called when the left mouse button is pressed down in the current view.
' A click is when both a down and an up event occurs in the view.
' X:         The x coordinate of the mouse pointer's location in window coordinates.
' Y:         The y coordinate of the mouse pointer's location in window coordinates.
' IsControl: True if the Ctrl key is currently pressed down.
' IsShift:   True if the Shift key is currently pressed down.
' ==================================================================================
'Sub View_OnLeftMouseButtonDown(X, Y, IsControl, IsShift)
'End Sub

' ==================================================================================
' Called when the left mouse button is released in the current view.
' A click is when both a down and an up event occurs in the view.
' X:         The x coordinate of the mouse pointer's location in window coordinates.
' Y:         The y coordinate of the mouse pointer's location in window coordinates.
' IsControl: True if the Ctrl key is currently pressed down.
' IsShift:   True if the Shift key is currently pressed down.
' ==================================================================================
'Sub View_OnLeftMouseButtonUp(X, Y, IsControl, IsShift)
'End Sub

' ==================================================================================
' Called when the left mouse button is double clicked in the current view.
' X:         The x coordinate of the mouse pointer's location in window coordinates.
' Y:         The y coordinate of the mouse pointer's location in window coordinates.
' IsControl: True if the Ctrl key is currently pressed down.
' IsShift:   True if the Shift key is currently pressed down.
' ==================================================================================
'Sub View_OnLeftMouseButtonDoubleClick(X, Y, IsControl, IsShift)
'End Sub

' ==================================================================================
' Called when the middle mouse button is pressed down in the current view.
' A click is when both a down and an up event occurs in the view.
' X:         The x coordinate of the mouse pointer's location in window coordinates.
' Y:         The y coordinate of the mouse pointer's location in window coordinates.
' IsControl: True if the Ctrl key is currently pressed down.
' IsShift:   True if the Shift key is currently pressed down.
' ==================================================================================
'Sub View_OnMiddleMouseButtonDown(X, Y, IsControl, IsShift)
'End Sub

' ==================================================================================
' Called when the middle mouse button is released in the current view.
' A click is when both a down and an up event occurs in the view.
' X:         The x coordinate of the mouse pointer's location in window coordinates.
' Y:         The y coordinate of the mouse pointer's location in window coordinates.
' IsControl: True if the Ctrl key is currently pressed down.
' IsShift:   True if the Shift key is currently pressed down.
' ==================================================================================
'Sub View_OnMiddleMouseButtonUp(X, Y, IsControl, IsShift)
'End Sub

' ==================================================================================
' Called when the middle mouse button is double clicked in the current view.
' X:         The x coordinate of the mouse pointer's location in window coordinates.
' Y:         The y coordinate of the mouse pointer's location in window coordinates.
' IsControl: True if the Ctrl key is currently pressed down.
' IsShift:   True if the Shift key is currently pressed down.
' ==================================================================================
'Sub View_OnMiddleMouseButtonDoubleClick(X, Y, IsControl, IsShift)
'End Sub

' ==================================================================================
' Called whenever the mouse pointer is moved in the current view.
' X:         The x coordinate of the mouse pointer's location in window coordinates.
' Y:         The y coordinate of the mouse pointer's location in window coordinates.
' IsControl: True if the Ctrl key is currently pressed down.
' IsShift:   True if the Shift key is currently pressed down.
' ==================================================================================
'Sub View_OnMouseMove(X, Y, IsControl, IsShift)
'End Sub

' ======================================================
' Called when something in the current view is selected.
' Selection: The view's selection object.
' ======================================================
'Sub View_OnSelect(Selection)
'End Sub

' ==========================================================
' Called after an overlay is inserted into the current view.
' OverlayName: The name of the overlay being inserted.
' ==========================================================
'Sub View_OnInsertOverlay(OverlayName)
'End Sub

' ==========================================================
' Called before an overlay is removed from the current view.
' OverlayName: The name of the overlay being removed.
' ==========================================================
'Sub View_OnRemoveOverlay(OverlayName)
'End Sub

' ==================================================================================
' Called after the size of the current view changes.
' ResizeType: One of the resize constants (hide, show, maximize, minimize, restore).
' Width:      The new width of the current view in pixels.
' Height:     The new height of the current view in pixels.
' ==================================================================================
'Sub View_OnSize(ResizeType, Width, Height)
'End Sub






