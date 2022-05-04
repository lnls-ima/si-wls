Import("auxiliary_functions.vbs")

Call NbTiCoil()

Sub NbTiCoil()

	Set objFSO = CreateObject("Scripting.FileSystemObject")

	If hasDocument() Then
		Set Doc = getDocument()
	Else
		MsgBox("The application does not have a document open.")
		Exit Sub
	End If

	FilePath = getDocumentPath(Doc)
	If isNull(FilePath) Then Exit Sub End If

	DocumentName = getDocumentName(Doc)
	If isNull(DocumentName) Then Exit Sub End If

	Dim BoxTitle
	BoxTitle = "Max. Field in the Coil"

	nproblem = GetProblemNumber(Doc, BoxTitle)
	If isNull(nproblem) Then Exit Sub End If

	DefaultName = ProcessDocumentName(DocumentName)

	Dim nproblems
	If isNumeric(nproblem) Then
		ReDim nproblems(0)
		nproblems(0) = nproblem
		DefaultName = DefaultName + "_Bmax_pid" + CStr(nproblem) + ".txt"
	Else
		nproblems = nproblem
		DefaultName = DefaultName + "_Bmax.txt"
	End If

	StepPos = GetVariableValue("Step (mm)", BoxTitle, "1", EmptyVar)
	If isNull(StepPos) Then Exit Sub End If

	Filename = GetVariableString("Enter the file name:", BoxTitle, DefaultName, EmptyVar)
	If isNull(Filename) Then Exit Sub End If

	FullFilename = objFSO.BuildPath(FilePath, Filename)

	Set objFile = objFSO.CreateTextFile(FullFilename, True)

	objFile.Write "Bp [T]" & vbTab & vbTab & "Bmax [T]" & vbTab & "Margin [%]" & vbTab & "FWHM [mm]" & vbCrlf

	text = "Bp [T]" & vbTab & vbTab & "Bmax [T]" & vbTab & vbTab & "Margin [%]" & vbTab & "FWHM [mm]" 
	
	For i=0 to Ubound(nproblems)
	 	np = nproblems(i)

		Set Mesh = Doc.getSolution.getMesh(np)
		Set Pblm = Doc.getProblem(np)
		Set AbsField = Doc.getSolution.getSystemField (Mesh, "|B|")

		'Parameters
		Call Pblm.getParameter("", "gap", gap)
		Call Pblm.getParameter("", "d", d)
		Call Pblm.getParameter("", "lcx0", lcx0)
		Call Pblm.getParameter("", "rpole0", rpole0)
		Call Pblm.getParameter("", "h_wire", hwire)
		Call Pblm.getParameter("", "n0_h", n0h)
		h0 = hwire*n0h
	
		xi = -((lcx0/2)+rpole0+d)
		yi = gap
	
		xf = (lcx0/2)+rpole0+d
		yf = gap+h0

		nptsx = (((xf - xi)^2)^(1/2))/StepPos + 1
		nptsy = (((yf - yi)^2)^(1/2))/StepPos + 1
		StepFwhm = 0.1
		nptsfwhm = 600/StepFwhm + 1

		a = (xf - xi)/nptsx
		b = (yf - yi)/nptsy

		Dim BArray
		ReDim BArray((nptsx+1)*(nptsy+1))

		Dim BMax
		Dim Marg

		For j=0 to nptsx
			x = xi + a*j

			If (x < -(lcx0/2)) Then
				z = (((rpole0+d)^2)-((x+(lcx0/2))^2))^(1/2)
			ElseIf (x > (lcx0/2)) Then
				z = (((rpole0+d)^2)-((x-(lcx0/2))^2))^(1/2)
			Else
				z = rpole0+d
			End If

			For k=0 to nptsy
				y = yi + b*k

				Call AbsField.getFieldAtPoint (x, y, z, AbsB)

				BArray(j*nptsy+k) = AbsB(0)
				
			Next

		Next

		BMax = Max(BArray)
		Call Doc.getSolution.getSystemField(Mesh,"B y").getFieldAtPoint(0, 0, 0, Bypeak)

		'Margin calculate
		Call Pblm.getParameter("", "i0", i0)
		Call Pblm.getParameter("", "SNbTi", SNbTi)
		Call Pblm.getParameter("", "Temp", T)
		Jscwire = i0/SNbTi
		Bcoil = BMax 
		Tc = 9.2
		Jcref = 3000
		Bc20 = 14.5
		C0 = 27.04
		alpha = 0.57
		beta =  0.9
		gamma = 2.32
		tnorm = T/Tc
		Bc2 = Bc20*(1-tnorm^1.7)

		For q=0 to 900
			Bc = 0.1+q*0.01
			bnorm = Bc/Bc2
			Jc = Jcref*C0*(Bc^(alpha-1))*((1-bnorm)^beta)*((1-tnorm^1.7)^gamma)/(Bc2^alpha)
			Jcc = (Jscwire/Bcoil)*Bc	
			If (Jcc >= Jc) Then
				Exit For
			End If
		Next

		Marg = 100*(1-Bcoil/Bc)

		For m=0 to nptsfwhm
			s = StepFwhm*m
			
			Call Doc.getSolution.getSystemField(Mesh, "B y").getFieldAtPoint(0, 0, s, by)
			If (Abs(by(0)) < Abs((Bypeak(0)/2))) Then
				fwhm = 2*s
				Exit For
			End If
		Next

		sp = Round(Bypeak(0), 4)
		sb = Round(BMax, 4)
		sbm = Round(Marg, 2)
		sfw = Round(fwhm, 1)

		objFile.Write sp & vbTab & vbTab & sb & vbTab & vbTab & sbm & vbTab & vbTab & sfw & vbCrlf

		text = text & vbCrLf & vbCrLf & sp & vbTab & vbTab & sb & vbTab & vbTab & sbm & vbTab & vbTab & sfw & vbCrlf

	Next

	objFile.Close
	MsgBox(text)

End Sub


Sub Import(strFile)

	Set objFSO = CreateObject("Scripting.FileSystemObject")
	Set wshShell = CreateObject("Wscript.Shell")
	strFile = WshShell.ExpandEnvironmentStrings(strFile)
	strFile = objFSO.GetAbsolutePathName(strFile)
	Set objFile = objFSO.OpenTextFile(strFile)
	strCode = objFile.ReadAll
	objFile.Close
	ExecuteGlobal strCode

End Sub